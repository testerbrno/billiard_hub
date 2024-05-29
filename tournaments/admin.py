from django.contrib import admin
from tournaments.models import Tournament, TournamentOrganizer, TournamentPlayer, Round, Match, MatchPlayer

admin.site.register([Tournament, TournamentOrganizer, TournamentPlayer, Round, Match, MatchPlayer])
