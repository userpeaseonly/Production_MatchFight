from django.db import models

GENDER_CHOICES = [
    (1, 'Male'),
    (0, 'Female'),
]

class Tournament(models.Model):
    gender = models.IntegerField(choices=GENDER_CHOICES)
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    min_weight = models.DecimalField(max_digits=5, decimal_places=2)
    max_weight = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.get_gender_display()} {self.min_age}-{self.max_age} years {self.min_weight}-{self.max_weight} kg"
