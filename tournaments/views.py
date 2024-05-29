from django.shortcuts import render
from django.views.generic import DetailView
from models import Tournament, Round, Match, MatchPlayer


class TournamentDetailView(DetailView):
    model = Tournament
    context_object_name = 'tournament'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tournament = self.get_object()
        context['rounds'] = tournament.round_set.all()
        return context

class RoundDetailView(DetailView):
    model = Round
    context_object_name = 'round'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        round = self.get_object()
        context['tournament'] = round.tournament
        return context

