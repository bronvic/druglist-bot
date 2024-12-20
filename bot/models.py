from django.contrib.postgres.fields import ArrayField
from django.db import models


# class Category(models.Model):
#     name = models.CharField(max_length=255, unique=True)
#     emoji = models.CharField(max_length=255, unique=True)
#
#     def __str__(self):
#         return f'{self.name} {self.emoji}'


class Medicine(models.Model):
    description = models.TextField()
    # categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return f"{self.description[:16]}"


class MedicineName(models.Model):
    name = models.CharField(max_length=255)
    description = models.ForeignKey(Medicine, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("name", "description")

    def __str__(self):
        return f"{self.name}: {self.description}"
