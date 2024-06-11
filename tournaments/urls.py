from django.urls import path
from django.views.generic import ListView
from tournaments.models import Tournament
from tournaments.views import TournamentDetailView, RoundDetailView, TournamentCreateView, TournamentUpdateView

urlpatterns = [
    path('', ListView.as_view(model=Tournament, template_name="./list/tournament_list.html"), name='tournaments'),
    path('<int:pk>/', TournamentDetailView.as_view(template_name="./detail/tournament_detail.html"), name='tournament_detail'),
    path('<int:tournament_pk>/round/<int:pk>/', RoundDetailView.as_view(template_name="./detail/round_detail.html"), name='round_detail'),

    # URL patterns for creating and updating tournaments
    path('create/', TournamentCreateView.as_view(template_name="./create/tournament_create.html"), name='tournament_create'),
    path('<int:pk>/update/', TournamentUpdateView.as_view(template_name="./create/tournament_create.html"), name='tournament_update'),

    # URL patterns for creating and updating rounds
    # path('<int:tournament_pk>/round/create/', RoundCreateView.as_view(template_name="./form/round_form.html"), name='round_create'),
    # path('<int:tournament_pk>/round/<int:pk>/update/', RoundUpdateView.as_view(template_name="./form/round_form.html"), name='round_update'),
]