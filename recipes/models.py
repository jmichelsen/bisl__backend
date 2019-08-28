from datetime import timedelta

# Django
from django.db import models

# local Django
from common.mixins.model import TimestampMixin
from .constants import DIFFICULTY_CHOICES


class Recipe(TimestampMixin, models.Model):
    title = models.CharField(max_length=100)
    ingredients = models.TextField(max_length=2000)
    preparation_process = models.TextField()
    preparation_time = models.DurationField(default=timedelta)
    number_of_portions = models.PositiveIntegerField(default=1)
    difficulty = models.SmallIntegerField(choices=DIFFICULTY_CHOICES)

    def __str__(self):
        return self.title


