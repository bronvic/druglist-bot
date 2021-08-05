from django.contrib.postgres.fields import ArrayField
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    smile = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.name} {self.smile}'


class Drug(models.Model):
    names = ArrayField(models.CharField(max_length=255, unique=True))
    description = models.TextField()
    categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return f'{self.names}'

