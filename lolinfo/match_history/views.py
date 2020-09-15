import requests, json, os, time
from django.shortcuts import render
from concurrent.futures import ThreadPoolExecutor
from django.http import HttpResponse, JsonResponse
from .forms import LoLAccount, Update
from django.views.decorators.csrf import csrf_exempt
from match_history.models import Summoner

api_key = 'RGAPI-cb04ac6f-576a-49fc-9f46-2610a5fe0fd7'
result = {'Win' : 'Victory', 'Fail' : 'Defeat'}

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'json/champions.json')
with open(filename) as f:
  champions = json.load(f) 
filename = os.path.join(dirname, 'json/spells.json')
with open(filename) as f:
  spells = json.load(f)

# Create your views here.
def index(request):
    if request.method == 'GET':
        form = LoLAccount()
        return render(request, "match_history_homepage.html", {'form' : form})

    if 'update-submit' in request.POST:
        form = Update(request.POST)
        if form.is_valid():
            summoner_name = form.cleaned_data['Summonername'].lower()
            region = form.cleaned_data['Region']
            return update(request, summoner_name, region)
        else:
            return HttpResponse("Wrong form input.")
            
    form = LoLAccount(request.POST)
    if form.is_valid():
        summoner_name = form.cleaned_data['Summonername'].lower()
        region = form.cleaned_data['Region']
        summoner = None
        try:
            summoner = Summoner.objects.get(name=summoner_name, region=region)
        except:
            try:
                summoner = create_summoner_entry(summoner_name, region)
            except Exception as e:
                print(e)
                return HttpResponse("Summoner not found.")

        summoner_info = {'name' : summoner.name, 'level' : summoner.level, 'icon_id' : summoner.icon_id, 'region' : summoner.region}
        ranked_info = {'rank' : summoner.rank, 'tier' : summoner.tier, 'winrate' : summoner.winrate, 'wins' : summoner.wins, 'losses' : summoner.losses, 'lp' : summoner.lp}
        return render(request, 'match_history_summoner.html', {'summoner_info' : summoner_info, 'ranked_info' : ranked_info, 'matches_history' : json.loads(summoner.matches_history)[0], 'form' : LoLAccount(), 'form1' : Update(name=summoner.name, region=summoner.region)})

@csrf_exempt
def expand(request):
    summoner = Summoner.objects.get(name=request.POST.get('name'))
    region = summoner.region
    summoner_name = summoner.name
    page = int(request.POST.get('id'))
    match_history = [None] * 10
    query = json.loads(summoner.matches_history)

    try:
        match_history = query[page]
    except:
        with ThreadPoolExecutor(max_workers=5) as executor:
            for i in range(10):
                executor.submit(api_call, region, match_history, i, json.loads(summoner.matches_ref)[page], summoner_name)

        query.append(match_history)
        summoner.matches_history = json.dumps(query)
        summoner.save()

    return JsonResponse(json.dumps(match_history), safe=False)

#########################################################################################################################################################
def api_call(region, match_history, th_id, matches_ref, summoner_name):
    try:
        url = f"https://{region}.api.riotgames.com/lol/match/v4/matches/{matches_ref[th_id]['gameId']}?api_key={api_key}"
        match = requests.get(url).json()
        cleaned_match = clean_match(summoner_name, match)
        match_history[th_id] = cleaned_match
    except Exception as e:
        print(e)

def update(request, summoner_name, region):
    Summoner.objects.filter(name=summoner_name, region=region).delete()
    summoner = create_summoner_entry(summoner_name, region)

    summoner_info = {'name' : summoner.name, 'level' : summoner.level, 'icon_id' : summoner.icon_id, 'region' : summoner.region}
    ranked_info = {'rank' : summoner.rank, 'tier' : summoner.tier, 'winrate' : summoner.winrate, 'wins' : summoner.wins, 'losses' : summoner.losses, 'lp' : summoner.lp}
    return render(request, 'match_history_summoner.html', {'summoner_info' : summoner_info, 'ranked_info' : ranked_info, 'matches_history' : json.loads(summoner.matches_history)[0], 'form' : LoLAccount(), 'form1' : Update(name=summoner.name, region=summoner.region)})

def create_summoner_entry(summoner_name, region):
    url = f"https://{region}.api.riotgames.com//lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={api_key}"
    summoner_info = requests.get(url).json()
    url = f"https://{region}.api.riotgames.com//lol/league/v4/entries/by-summoner/{summoner_info['id']}?api_key={api_key}"
    ranked_info = requests.get(url).json()
    url = f"https://{region}.api.riotgames.com/lol/match/v4/matchlists/by-account/{summoner_info['accountId']}?api_key={api_key}"
    matches_ref = requests.get(url).json()
    chunks = [matches_ref['matches'][x:x+10] for x in range(0, len(matches_ref['matches']), 10)]

    summoner = None
    if ranked_info:
        ranked_info = ranked_info[0]
        ranked_info['winrate'] = float(ranked_info['wins']) / (float(ranked_info['losses']) + float(ranked_info['wins'])) * 100
        summoner = Summoner(name=summoner_name, region=region, icon_id=summoner_info['profileIconId'], level=summoner_info['summonerLevel'], matches_ref=json.dumps(chunks), lp=ranked_info['leaguePoints'], rank=ranked_info['rank'], tier=ranked_info['tier'], wins=ranked_info['wins'], losses=ranked_info['losses'], winrate=ranked_info['winrate'])
    else:
        summoner = Summoner(name=summoner_name, region=region, icon_id=summoner_info['profileIconId'], level=summoner_info['summonerLevel'], matches_ref=json.dumps(chunks))

    summoner.matches_history = json.dumps(get_initial_history(summoner_name, json.loads(summoner.matches_ref), region, summoner))
    summoner.save()
    return summoner

def clean_match(summoner_name, match):
    cleaned_match = {'duration' :  {'minutes': int(match['gameDuration'] / 60), "seconds" : match['gameDuration'] % 60}, 'mode' : match['gameMode']}
    red = {'players' : [], 'result' : None}
    blue = {'players' : [], 'result' : None}

    for participant in match['participants']:
        player = get_player(participant, match['participantIdentities'])
        if player['summoner_name'].lower() == summoner_name:
            cleaned_match['main'] = player
        if participant['teamId'] == 100: 
            blue['players'].append(player)
        else:
            red['players'].append(player)

    for team in match['teams']:
        if team['teamId'] == 100:
            blue['result'] = result[team['win']]
            if cleaned_match['main'] in blue['players']:
                cleaned_match['result'] = blue['result']
        else:
            red['result'] = result[team['win']]
            if cleaned_match['main'] in red['players']:
                cleaned_match['result'] = red['result']

    cleaned_match['red'] = red
    cleaned_match['blue'] = blue
    return cleaned_match
    
def get_initial_history(summoner_name, matches_ref, region, summoner):
    match_history = []
    temp = [None] * 10
    with ThreadPoolExecutor(max_workers=5) as executor:
        for i in range(10):
            executor.submit(api_call, region, temp, i, json.loads(summoner.matches_ref)[0], summoner_name)
    match_history.append(temp)
    return match_history
   
def get_kda(stats):
    return {'kills' : stats['kills'], 'deaths' : stats['deaths'], 'assists' : stats['assists']}

def get_items(stats):
    items = []
    for x in range(6):
        if stats[f'item{x}']:
            items.append(stats[f'item{x}'])
    return items

def get_champ(champ_id):
    for champion in champions['data'].values():
        if (int(champion['key']) == champ_id):
            return champion['name']

def get_spell(spell_id):
    for spell in spells['data'].values():
        if (int(spell['key']) == spell_id):
            return {'id' : spell['id'], 'name' : spell['name']}

def get_player(participant, participant_ids):
    player = {}
    for entry in participant_ids:
        if entry['participantId'] == participant['participantId']:
            player['summoner_name'] = entry['player']['summonerName']

    player['champion'] = get_champ(participant['championId'])
    player['spells'] = [get_spell(participant['spell1Id']), get_spell(participant['spell2Id'])]
    player['KDA'] = get_kda(participant['stats'])
    player['items'] = get_items(participant['stats'])
    player['level'] = participant['stats']['champLevel']
    player['damage'] = participant['stats']['totalDamageDealtToChampions']
    player['CS'] = participant['stats']['totalMinionsKilled']
    return player
#########################################################################################################################################################