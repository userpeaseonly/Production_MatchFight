from django.db import models

class Competition(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name
