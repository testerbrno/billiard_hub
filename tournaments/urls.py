from django.urls import path
from django.views.generic import ListView
from tournaments.models import Tournament
from tournaments.views import TournamentDetailView, RoundDetailView, TournamentCreateView, TournamentUpdateView, RoundCreateView, MatchCreateView, MatchPlayerCreateView, MatchPlayerUpdateView, RoundUpdateView, AddFormView, DeleteFormView

urlpatterns = [
    path('', ListView.as_view(model=Tournament, template_name="./list/tournament_list.html"), name='tournaments'),
    path('<int:tournament_pk>/', TournamentDetailView.as_view(template_name="./detail/tournament_detail.html"), name='tournament_detail'),
    path('<int:tournament_pk>/<int:round_pk>/', RoundDetailView.as_view(template_name="./detail/round_with_matches.html"), name='round_detail'),

    # URL patterns for creating and updating tournaments
    path('create/', TournamentCreateView.as_view(), name='tournament_create'),
    path('<int:tournament_pk>/update/', TournamentUpdateView.as_view(template_name="./create/tournament_create.html"), name='tournament_update'),

    # URL patterns for creating and updating rounds
    path('<int:tournament_pk>/<str:form_class>/create/', RoundCreateView.as_view(template_name="./create/round_form.html"), name='round_create'),
    path('<int:tournament_pk>/<int:round_pk>/update/', RoundUpdateView.as_view(template_name="./update/round_update.html"), name='round_update'),
    path('<int:tournament_pk>/<int:round_pk>/<str:form_class>/create/', MatchCreateView.as_view(), name='match_create'),
    path('<int:tournament_pk>/<int:round_pk>/<int:match_pk>/<str:form_class>/create/', MatchPlayerCreateView.as_view(template_name="./create/match_player_form.html"), name='matchplayer_create'),
    path('<int:tournament_pk>/<int:round_pk>/<int:match_pk>/<int:matchplayer_pk>/update/', MatchPlayerUpdateView.as_view(template_name='./update/match_player_update.html'), name='matchplayer_update'),

    # URL pattern for adding formsets using HTMX
    path('<str:form_class>/add_form/', AddFormView.as_view(), name='add_form'),
    path('delete_form/', DeleteFormView.as_view(), name='delete_form'),
]