from django.shortcuts import render
from django.views.generic import DetailView
from tournaments.models import Tournament, TournamentPlayer, TournamentOrganizer, Round, Match, MatchPlayer


class TournamentDetailView(DetailView):
    model = Tournament
    context_object_name = 'tournament'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        this_tournament = self.get_object()
        context['rounds'] = this_tournament.round_set.all()
        context['organizers'] = TournamentOrganizer.objects.filter(tournament=this_tournament).select_related('organizer')
        context['players'] = TournamentPlayer.objects.filter(tournament=this_tournament).select_related('player')

        return context

class RoundDetailView(DetailView):
    model = Round
    context_object_name = 'round'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        round = self.get_object()
        context['tournament'] = round.tournament
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if 'tournament_pk' in self.kwargs:
            queryset = queryset.filter(tournament_id=self.kwargs['tournament_pk'])
        return queryset
