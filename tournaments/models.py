from django.db import models
from django.core.exceptions import ValidationError
from players.models import Player

class Tournament(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    organizators = models.ManyToManyField(Player, related_name='organizing_t')
    players = models.ManyToManyField(Player, related_name='tournaments')

    def __str__(self):
        return self.name

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
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def check_player_in_tournament(self):
        tournament_players = self.match.round.tournament.players.all()
        if self.player not in tournament_players:
            raise ValidationError("The player is not part of the tournament players")

    def save(self, *args, **kwargs):
        self.check_player_in_tournament()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.player.name} in Match ID:{self.match.pk}"