from django.db import models
from common.mixins.model import TimestampMixin
# Create your models here.

class Recipe(TimestampMixin, models.Model):

    EASY = 1
    MEDIUM = 2
    HARD = 3
    DIFFICULTIES = (
        (EASY, 'easy'),
        (MEDIUM, 'medium'),
        (HARD, 'hard'),
    )

    title = models.CharField(max_length=100)
    ingredients = models.TextField(max_length=2000)
    preparation_process = models.TextField()
    preparation_time = models.DurationField()
    number_of_portions = models.PositiveIntegerField(default=1)
    difficulty = models.SmallIntegerField(choices=DIFFICULTIES)

    class Meta:
        verbose_name_plural = 'recipes'

    def __str__(self):
        return self.title[:50]

