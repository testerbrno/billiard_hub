from django.urls import path
from views import TournamentDetailView, RoundDetailView

urlpatterns = [
    path('tournament/<int:tournament_id>/', TournamentDetailView.as_view(), name='round_detail'),
    path('tournament/<int:tournament_id>/round/<int:round_id>/', RoundDetailView.as_view(), name='round_detail'),
]