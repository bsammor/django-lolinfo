function expand() {
    var name = document.getElementsByName("Summonername")[1].value
    var region = document.getElementsByName("Region")[1].value
    var id = document.getElementsByClassName("match-history-blk").length

    
    jsonObj = {name : name, region : region, id : id}
    $.post("/lolinfo/expand/", jsonObj, function(data) {
        var outer = document.createElement("div"); 
        outer.className = "match-history-blk"

        response = JSON.parse(data)
        console.log(response)
        for (var i = 0; i < response.length; i++)
        {
            var inner = document.createElement("div"); 
            inner.className = "match"
            var inner_inner0 = document.createElement("div"); 
            inner_inner0.className = "main"
            var inner_inner1 = document.createElement("div"); 
            inner_inner1.className = "dropdown"

            //main block elements
            var textnode = document.createTextNode("Mode: " + response[i].mode + " ");
            inner_inner0.append(textnode);
            var textnode = document.createTextNode("Duration: " + response[i].duration.minutes + "m " + response[i].duration.seconds + "s ");
            inner_inner0.append(textnode);
            var textnode = document.createTextNode("Result: " + response[i].result);
            inner_inner0.append(textnode);
            var table = document.createElement("table")
            inner_inner0.append(table)
            var tbody = document.createElement("tbody")
            table.append(tbody)
            var tr = tbody.insertRow();

            var td = tr.insertCell();
            var profile = document.createElement("img");
            var champion = (response[i].main.champion.replace(/'/g, '')).replace(/\s/g, '')
            profile.className = "img-thumbnail"
            profile.src="https://opgg-static.akamaized.net/images/lol/champion/" + champion + ".png?image=q_auto,w_46&v=1596679559"
            profile.setAttribute("width", "55px") 
            profile.setAttribute("height", "55px") 
            var textnode = document.createTextNode(" " + response[i].main.level);
            td.append(profile);
            td.append(textnode)


            var td = tr.insertCell();
            for (var j = 0; j < response[i].main.spells.length; j++) {
              var item = document.createElement("img");
              item.className = "img-thumbnail"
              item.src="https://ddragon.leagueoflegends.com/cdn/10.16.1/img/spell/" + response[i].main.spells[j].id + ".png"
              item.setAttribute("width", "30px") 
              item.setAttribute("height", "30px") 
              td.append(item);
              if (j == 0){td.append(document.createElement("br"))}
            }

            var td = tr.insertCell();
            var temp = "KDA: " + response[i].main.KDA.kills + "/" + response[i].main.KDA.deaths + "/" + response[i].main.KDA.assists
            var textnode = document.createTextNode(temp);
            td.append(textnode);

            var td = tr.insertCell();
            var temp = "CS: " + response[i].main.CS
            var textnode = document.createTextNode(temp);
            td.append(textnode);

            var td = tr.insertCell();
            var temp = "Damage: " + response[i].main.damage
            var textnode = document.createTextNode(temp);
            td.append(textnode);

            var td = tr.insertCell();
            for (var j = 0; j < response[i].main.items.length; j++) {
                var item = document.createElement("img");
                item.className = "img-thumbnail"
                item.src="https://ddragon.leagueoflegends.com/cdn/10.16.1/img/item/" + response[i].main.items[j] + ".png"
                item.setAttribute("width", "40px") 
                item.setAttribute("height", "40px") 
                td.append(item);
            }
            //////////////////////////////////////////////////////////////////////////////////////////////////////


            inner.append(inner_inner0)
            inner.append(inner_inner1)
            outer.append(inner)
            var br = document.createElement('br');
            outer.append(br);
        }
        var main = document.getElementsByClassName("match-history")[0]
        main.append(outer)
    });
}

function toggle_match(id) {
  var x = document.getElementById(id);
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}