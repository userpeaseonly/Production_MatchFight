from django.db import models
from competitions.models import Competition
from tournaments.models import Tournament
from participants.models import Participant

STAGE_CHOICES = [
    ('final', 'Final'),
    ('half-final', 'Half-Final'),
    ('quarter-final', 'Quarter-Final'),
]

class FinalsParticipant(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='finals_participants')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='finals_participants')
    place = models.IntegerField(null=True, blank=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='finals_participants')

    def __str__(self):
        return f"{self.participant} - Place {self.place}"

class FinalsPair(models.Model):
    participant1 = models.ForeignKey(FinalsParticipant, on_delete=models.CASCADE, related_name='finals_participant1_pairs')
    participant2 = models.ForeignKey(FinalsParticipant, on_delete=models.CASCADE, related_name='finals_participant2_pairs', null=True, blank=True)
    stage = models.CharField(max_length=50, choices=STAGE_CHOICES)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='finals_pairs')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='finals_pairs')
    winner = models.ForeignKey(FinalsParticipant, on_delete=models.CASCADE, related_name='finals_won_pairs', null=True, blank=True)

    def __str__(self):
        return f"{self.participant1} vs {self.participant2} - Stage {self.stage}"
