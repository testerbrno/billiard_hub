from django.urls import path
from django.views.generic import ListView
from tournaments.models import Tournament
from tournaments.views import TournamentDetailView, RoundDetailView, TournamentCreateView, TournamentUpdateView, RoundCreateView, MatchCreateView, MatchPlayerCreateView, MatchPlayerUpdateView

urlpatterns = [
    path('', ListView.as_view(model=Tournament, template_name="./list/tournament_list.html"), name='tournaments'),
    path('<int:tournament_pk>/', TournamentDetailView.as_view(template_name="./detail/tournament_detail.html"), name='tournament_detail'),
    path('<int:tournament_pk>/<int:round_pk>/', RoundDetailView.as_view(template_name="./detail/round_detail.html"), name='round_detail'),

    # URL patterns for creating and updating tournaments
    path('create/', TournamentCreateView.as_view(template_name="./create/tournament_create.html"), name='tournament_create'),
    path('<int:tournament_pk>/update/', TournamentUpdateView.as_view(template_name="./create/tournament_create.html"), name='tournament_update'),

    # URL patterns for creating and updating rounds
    path('<int:tournament_pk>/round/create/', RoundCreateView.as_view(template_name="./create/round_form.html"), name='round_create'),
    # path('<int:tournament_pk>/round/<int:pk>/update/', RoundUpdateView.as_view(template_name="./form/round_form.html"), name='round_update'),
    path('<int:tournament_pk>/<int:round_pk>/match/create/', MatchCreateView.as_view(template_name="./create/match_form.html"), name='match_create'),
    path('<int:tournament_pk>/<int:round_pk>/<int:match_pk>/matchplayer/create/', MatchPlayerCreateView.as_view(template_name="./create/match_player_form.html"), name='matchplayer_create'),
    path('<int:tournament_pk>/<int:round_pk>/<int:match_pk>/<int:matchplayer_pk>/update/', MatchPlayerUpdateView.as_view(template_name='./update/match_player_update.html'), name='matchplayer_update'),
]