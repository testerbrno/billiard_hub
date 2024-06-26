from django.db import models
from django.core.exceptions import ValidationError
from players.models import Player

class Tournament(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)

    def __str__(self):
        return self.name

class TournamentOrganizer(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    organizer = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.organizer}"

class TournamentPlayer(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.player}"

class Round(models.Model):
    name = models.CharField(max_length=100)
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Match(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    referee = models.ForeignKey(Player, on_delete=models.RESTRICT, related_name='matches_refereed')

    def __str__(self):
        return f"Match ID:{self.pk}"

class MatchPlayer(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="match_players")
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="player_matches")
    score = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.player.username} in Match ID:{self.match.pk}"
    
# u každého zápasu musí být sledovány i jednotlivé tahy ()