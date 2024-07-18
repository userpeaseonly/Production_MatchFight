from django.db import models
from participants.models import Participant
from competitions.models import Competition
from tournaments.models import Tournament

class Pair(models.Model):
    participant1 = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='participant1_pairs')
    participant2 = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='participant2_pairs', null=True, blank=True)
    level = models.IntegerField()
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='pairs')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='pairs')
    winner = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='won_pairs', null=True, blank=True)

    def __str__(self):
        return f"{self.participant1} vs {self.participant2} - Level {self.level}"

