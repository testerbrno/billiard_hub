from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django import forms
from django.core.exceptions import ValidationError
from django.views.generic import DetailView, CreateView, UpdateView
from tournaments.models import Tournament, TournamentPlayer, TournamentOrganizer, Round, Match, MatchPlayer
from tournaments.forms import TournamentForm
from players.models import Player

class TournamentDetailView(DetailView):
    model = Tournament
    context_object_name = 'tournament'

    def get_object(self, queryset=None):
        return Tournament.objects.get(pk=self.kwargs['tournament_pk'])

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

    def get_object(self, queryset=None):
        return Round.objects.get(pk=self.kwargs['round_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        this_round = self.get_object()
        context['tournament'] = this_round.tournament
        context['matches'] = Match.objects.filter(round=this_round).select_related('referee')
        context['rounds'] = this_round.tournament.round_set.all()
        for one_match in context['matches']:
            players = MatchPlayer.objects.filter(match=one_match).select_related('player')
            one_match.players = players if players.exists() else []
        return context

class TournamentCreateView(CreateView):
    model = Tournament
    form_class = TournamentForm
    success_url = reverse_lazy('tournaments')

class TournamentUpdateView(UpdateView):
    model = Tournament
    form_class = TournamentForm

    def get_success_url(self):
        return reverse('tournament_detail', kwargs={'pk': self.object.pk})

class RoundCreateView(CreateView):
    model = Round
    fields = ['name', 'attachment']

    def form_valid(self, form):
        tournament = Tournament.objects.get(pk=self.kwargs['tournament_pk'])
        form.instance.tournament = tournament
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tournament_detail', kwargs={'tournament_pk': self.object.tournament.pk})

class MatchCreateView(CreateView):
    model = Match
    fields = ['referee']

    def form_valid(self, form):
        round_instance = Round.objects.get(pk=self.kwargs['round_pk'])
        form.instance.round = round_instance
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('round_detail', kwargs={
            'tournament_pk': self.object.round.tournament.pk,
            'round_pk': self.object.round.pk
        })

class MatchPlayerValidationMixin:
    def clean_match_player(self, instance):
        tournament_players = instance.match.round.tournament.tournamentplayer_set.all()
        if instance.player not in [tp.player for tp in tournament_players]:
            raise ValidationError("The player is not part of the tournament players")

    def form_valid(self, form):
        if 'match_pk' in self.kwargs:
            match_instance = Match.objects.get(pk=self.kwargs['match_pk'])
            form.instance.match = match_instance
        try:
            self.clean_match_player(form.instance)
        except ValidationError as e:
            form.add_error(None, e)
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('round_detail', kwargs={
            'tournament_pk': self.object.match.round.tournament.pk,
            'round_pk': self.object.match.round.pk
        })

class MatchPlayerCreateView(MatchPlayerValidationMixin, CreateView):
    model = MatchPlayer
    fields = ['player', 'score']

class MatchPlayerUpdateView(MatchPlayerValidationMixin, UpdateView):
    model = MatchPlayer
    fields = ['player', 'score']

    def get_object(self, queryset=None):
        return MatchPlayer.objects.get(pk=self.kwargs['matchplayer_pk'])