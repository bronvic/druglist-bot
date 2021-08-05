from django.contrib.postgres.fields import ArrayField
from django.db import models

class Drug(models.Model):
    names = ArrayField(models.CharField(max_length=255, unique=True))
    description = models.TextField()

    def __str__(self):
        return f'{self.names}'

