from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django import forms
from django.core.exceptions import ValidationError
from django.views.generic import TemplateView
from django.views.generic import DetailView, View, UpdateView, CreateView
from django.template.response import TemplateResponse
from tournaments.models import Tournament, TournamentPlayer, TournamentOrganizer, Round, Match, MatchPlayer
from tournaments.forms import TournamentForm, TournamentOrganizerForm, TournamentPlayerForm, RoundForm, MatchForm, MatchPlayerForm
from players.models import Player

LIST_FORM_CLASSES = {
    'tournament': TournamentForm,
    'organizer': TournamentOrganizerForm,
    'player': TournamentPlayerForm,
    'round': RoundForm,
    'match': MatchForm,
    'competitor': MatchPlayerForm,
}
    
class TournamentContextMixin:
    def get_tournament(self):
        return Tournament.objects.get(pk=self.kwargs['tournament_pk'])

    def get_round(self):
        return Round.objects.get(pk=self.kwargs['round_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'tournament_pk' in self.kwargs:
            tournament = self.get_tournament()
            context['tournament'] = tournament
            context['rounds'] = tournament.round_set.all()
            context['organizers'] = TournamentOrganizer.objects.filter(tournament=tournament).select_related('organizer')
            context['players'] = TournamentPlayer.objects.filter(tournament=tournament).select_related('player')
        if 'round_pk' in self.kwargs:
            round_instance = self.get_round()
            context['round'] = round_instance
            context['matches'] = Match.objects.filter(round=round_instance).select_related('referee')
            for one_match in context['matches']:
                players = MatchPlayer.objects.filter(match=one_match).select_related('player')
                one_match.players = players if players.exists() else []
        return context

class DynamicFormMixin:
    def get_form_class(self):
        form_type = self.kwargs.get('form_class')
        form_class = LIST_FORM_CLASSES.get(form_type)
        if form_class is None:
            raise ValueError(f"Form class '{form_type}' not found.")
        return form_class

    def get_form(self, **kwargs):
        form_class = self.get_form_class()
        return form_class(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_class = self.get_form_class()
        context['form'] = form_class()
        return context

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.get_success_url())

# combined create views

class TournamentCreateView(TournamentContextMixin, View):
    success_url = reverse_lazy('tournaments')
    tournament_instance = None
    form_classes = {
    'tournament': TournamentForm,
    'organizer': TournamentOrganizerForm,
    'player': TournamentPlayerForm,
    'round': RoundForm,
}

    def get(self, request, *args, **kwargs):
        return render(request, './create/tournament_create.html')

    def post(self, request, *args, **kwargs):
        errors = {}
        tournament_instance = None
        print(f"toto je obsah request.POST(77): {request.POST}")

        if any(key.startswith('tournament') for key, value in request.POST.items()):
            for form_type, form_class in self.form_classes.items():
                prefix = f"{form_type}_"
                related_form_data = {key.split('-', 1)[1]: value for key, value in request.POST.items() if key.startswith(prefix)}
                print(f"toto je obsah related_form_data(83): {related_form_data}")
                related_form = form_class(related_form_data)
                print(f"toto je obsah related_form(85): {related_form}")
                
                if related_form.is_valid():
                    related_instance = related_form.save(commit=False)
                    print(f"toto je obsah related_instance(89): {related_instance}")
                    
                    if form_class == TournamentForm:
                        related_instance.save()
                        self.tournament_instance = related_instance
                        print(f"toto je obsah tournament_instance(94): {self.tournament_instance}")
                    else:
                        if self.tournament_instance is not None:
                            print(f"toto je obsah related_instance(98): {related_instance}")
                            related_instance.tournament = self.tournament_instance
                            print(f"toto je obsah related_instance(100): {related_instance}")
                            print(f"toto je obsah related_instance.tournament(101): {related_instance.tournament}")
                            related_instance.save()
                else:
                    errors[form_type] = related_form.errors
                    print(f"toto je obsah related_form.errors(102): {related_form.errors}")

            if errors:
                # Vrátíme chybové informace
                return render(request, './create/tournament_create.html', {'errors': errors})

            return redirect(self.success_url)


class MatchCreateView(TournamentContextMixin, View):
    form_classes = {
    'match': MatchForm,
    'competitor': MatchPlayerForm,
}

    def get_success_url(self):
        return reverse('round_detail', kwargs={
            'tournament_pk': self.tournament_pk.pk,
            'round_pk': self.round_pk
        })

    def get(self, request, *args, **kwargs):
        return render(request, './create/match_form.html')

    def post(self, request, *args, **kwargs):
        errors = {}
        self.match_instance = None

        if any(key.startswith('match') for key, value in request.POST.items()):
            self.round_pk = kwargs.get('round_pk')
            self.round_instance = get_object_or_404(Round, pk=self.round_pk)
            self.tournament_pk = self.round_instance.tournament
            for form_type, form_class in self.form_classes.items():
                prefix = f"{form_type}_"
                related_form_data = {key.split('-', 1)[1]: value for key, value in request.POST.items() if key.startswith(prefix)}
                related_form = form_class(related_form_data)
                
                if related_form.is_valid():
                    related_instance = related_form.save(commit=False)
                    
                    if form_class == MatchForm:
                        related_instance.round = self.round_instance
                        related_instance.save()
                        self.match_instance = related_instance
                    else:
                        if self.match_instance is not None:
                            related_instance.match = self.match_instance
                            related_instance.save()
                else:
                    errors[form_type] = related_form.errors

            if errors:
                # Vrátíme chybové informace
                return render(request, './create/match_form.html', {'errors': errors})

            success_url_obtained = self.get_success_url()
            return redirect(success_url_obtained)

class AddFormView(DynamicFormMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        if not request.session.get('form_counter'):
            request.session['form_counter'] = 0
        request.session['form_counter'] += 1
        form_class = self.kwargs.get('form_class')
        form_prefix = f"{form_class}_{request.session['form_counter']}"
        form = self.get_form(prefix=form_prefix)
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, './partials/form.html', context)

class DeleteFormView(DynamicFormMixin, TemplateView):
    def delete(self, request, *args, **kwargs):
        
        return HttpResponse()

# single create views
class TournamentDetailView(TournamentContextMixin, DetailView):
    model = Tournament
    context_object_name = 'tournament'

    def get_object(self, queryset=None):
        return self.get_tournament()

class RoundDetailView(TournamentContextMixin, DetailView):
    model = Round
    context_object_name = 'round'

    def get_object(self, queryset=None):
        return self.get_round()

# class TournamentCreateView(TournamentContextMixin, CreateView):
#     model = Tournament
#     form_class = TournamentForm
#     success_url = reverse_lazy('tournaments')

class TournamentUpdateView(TournamentContextMixin, UpdateView):
    model = Tournament
    form_class = TournamentForm

    def get_success_url(self):
        return reverse('tournament_detail', kwargs={'pk': self.object.pk})

class RoundCreateView(TournamentContextMixin, CreateView):
    model = Round
    fields = ['name', 'attachment']

    def form_valid(self, form):
        tournament = self.get_tournament()
        form.instance.tournament = tournament
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tournament_detail', kwargs={'tournament_pk': self.object.tournament.pk})

# class MatchCreateView(TournamentContextMixin, CreateView):
#     model = Match
#     fields = ['referee']

#     def form_valid(self, form):
#         round_instance = self.get_round()
#         form.instance.round = round_instance
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse('round_detail', kwargs={
#             'tournament_pk': self.object.round.tournament.pk,
#             'round_pk': self.object.round.pk
#         })

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

class MatchPlayerCreateView(TournamentContextMixin, MatchPlayerValidationMixin, CreateView):
    model = MatchPlayer
    fields = ['player', 'score']

class MatchPlayerUpdateView(TournamentContextMixin, MatchPlayerValidationMixin, UpdateView):
    model = MatchPlayer
    fields = ['player', 'score']

    def get_object(self, queryset=None):
        return MatchPlayer.objects.get(pk=self.kwargs['matchplayer_pk'])

class RoundUpdateView(TournamentContextMixin, UpdateView):
    model = Round
    fields = ['name', 'attachment']
    context_object_name = 'round'

    def get_object(self, queryset=None):
        return self.get_round()

    def form_valid(self, form):
        # Aktualizujeme turnaj, pokud je to potřeba
        tournament = self.get_tournament()
        form.instance.tournament = tournament
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tournament_detail', kwargs={'tournament_pk': self.object.tournament.pk})
