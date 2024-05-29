from django.urls import path
from tournaments.views import TournamentDetailView, RoundDetailView

urlpatterns = [
    path('<int:pk>/', TournamentDetailView.as_view(template_name="./detail/tournament_detail_block.html"), name='tournament_detail'),
    path('<int:tournament_pk>/round/<int:pk>/', RoundDetailView.as_view(), name='round_detail'),
]