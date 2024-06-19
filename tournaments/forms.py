from django import forms
from django.forms import inlineformset_factory
from tournaments.models import Tournament, TournamentOrganizer, TournamentPlayer, Round, Match, MatchPlayer
from players.models import Player

class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'start_date', 'end_date', 'attachment']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class TournamentOrganizerForm(forms.ModelForm):
    class Meta:
        model = TournamentOrganizer
        fields = ['organizer']

class TournamentPlayerForm(forms.ModelForm):
    class Meta:
        model = TournamentPlayer
        fields = ['player']

class RoundForm(forms.ModelForm):
    class Meta:
        model = Round
        fields = ['name', 'attachment']

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['referee']

class MatchPlayerForm(forms.ModelForm):
    class Meta:
        model = MatchPlayer
        fields = ['player', 'score']
