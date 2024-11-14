from django import forms
from .models import Voter

class VoterFilterForm(forms.Form):
    partyAffiliation = forms.ChoiceField(choices=[('', 'Any')] + [(party, party) for party in Voter.objects.values_list('party_affiliation', flat=True).distinct()], required=False)
    minDateOfBirth = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2024)), required=False)
    maxDateOfBirth = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2024)), required=False)
    voterScore = forms.ChoiceField(choices=[('', 'Any')] + [(str(score), str(score)) for score in range(6)], required=False)
    v20State = forms.BooleanField(required=False)
    v21Town = forms.BooleanField(required=False)
    v21Primary = forms.BooleanField(required=False)
    v22General = forms.BooleanField(required=False)
    v23Town = forms.BooleanField(required=False)