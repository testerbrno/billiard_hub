from django import forms
from tournaments.models import Tournament
from players.models import Player

class TournamentForm(forms.ModelForm):
    organizers = forms.ModelMultipleChoiceField(
        queryset=Player.objects.all(), 
        required=True, 
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'organizer-search'}),
    )
    players = forms.ModelMultipleChoiceField(
        queryset=Player.objects.all(), 
        required=False, 
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'player-search'})
    )

    class Meta:
        model = Tournament
        fields = ['name', 'start_date', 'end_date', 'attachment', 'organizers', 'players']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
