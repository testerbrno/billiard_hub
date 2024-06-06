from django.shortcuts import render
from django.urls import reverse_lazy
from django import forms
from django.views.generic import DetailView, CreateView, UpdateView
from tournaments.models import Tournament, TournamentPlayer, TournamentOrganizer, Round, Match, MatchPlayer
from tournaments.forms import TournamentForm
from players.models import Player


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
        this_round = self.get_object()
        context['tournament'] = this_round.tournament
        context['matches'] = Match.objects.filter(round=this_round).select_related('referee')
        context['rounds'] = this_round.tournament.round_set.all()
        for one_match in context['matches']:
            one_match.players = MatchPlayer.objects.filter(match=one_match).select_related('player')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if 'tournament_pk' in self.kwargs:
            queryset = queryset.filter(tournament_id=self.kwargs['tournament_pk'])
        return queryset

class TournamentCreateUpdateMixin:
    form_class = TournamentForm
    success_url = reverse_lazy('tournament_detail')
    context_object_name = 'tournament'

    def form_valid(self, form):
        response = super().form_valid(form)
        organizer = form.cleaned_data['organizers']
        players = form.cleaned_data['players']

        # Create TournamentOrganizer instance
        for one_organizer in organizer:
            self.object.organizers.add(one_organizer)

        # Create TournamentPlayer instances for each selected player
        for one_player in players:
            self.object.players.add(one_player)

        return response

class TournamentCreateView(TournamentCreateUpdateMixin, CreateView):
    model = Tournament

class TournamentUpdateView(TournamentCreateUpdateMixin, UpdateView):
    model = Tournament