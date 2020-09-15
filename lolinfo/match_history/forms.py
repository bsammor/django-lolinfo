from django import forms

class LoLAccount(forms.Form):
    Summonername = forms.CharField(max_length=100, widget=forms.TextInput())
    Region = forms.ChoiceField(choices=[("na1", "NA"), ("euw1", "EUW"), ("eun1", "EUNE")])

class Update(forms.Form):
    def __init__(self, *args, **kwargs):
        name = kwargs.pop('name', '')
        region = kwargs.pop('region', '')
        super(Update, self).__init__(*args, **kwargs)
        self.fields["Summonername"].widget.attrs['value'] = name
        self.fields["Region"].widget.attrs['value'] = region

    Summonername = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'type' : 'hidden'}))
    Region = forms.ChoiceField(choices=[("na1", "NA"), ("euw1", "EUW"), ("eun1", "EUNE")], widget=forms.TextInput(attrs={'type' : 'hidden'}))