from django.db import models
from competitions.models import Competition

GENDER_CHOICES = [
    (1, 'Male'),
    (0, 'Female'),
]

class Participant(models.Model):
    name = models.CharField(max_length=255)
    gender = models.IntegerField(choices=GENDER_CHOICES)
    age = models.IntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='participants/', blank=True, null=True)
    unique_id = models.CharField(max_length=255, unique=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='participants')
    miss = models.BooleanField(default=False)

    def __str__(self):
        return self.name
