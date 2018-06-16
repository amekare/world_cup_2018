from django import forms
from dashboard.models import Bet


class BetForm(forms.ModelForm):
    class Meta:
        model = Bet
        fields = ['source', 'match', 'team1', 'team2', 'goals_team1', 'goals_team2']
        widgets = {
            'source': forms.RadioSelect,
        }