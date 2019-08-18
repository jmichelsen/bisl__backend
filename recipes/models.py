from datetime import timedelta

# Django
from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models
from django.utils.functional import cached_property
from django_measurement.models import MeasurementField
from measurement.measures import Volume, Weight, Energy

# local app
from common.models import BaseModel
from common.utils import get_system_user
from recipes.constants import DIFFICULTY_CHOICES


class Recipe(BaseModel):
    """
    A Recipe containing the following information:
    """
    user = models.ForeignKey(AUTH_USER_MODEL, models.SET(get_system_user), related_name='recipes')
    users_who_made_this = models.ManyToManyField(AUTH_USER_MODEL, related_name='made_recipes')
    title = models.CharField(max_length=100)
    description = models.TextField()
    ingredients = models.ManyToManyField('recipes.Ingredient', related_name='in_recipes')
    preparation_time = models.DurationField(default=timedelta)
    cook_time = models.DurationField(default=timedelta)
    servings = models.PositiveSmallIntegerField(default=1)
    max_servings = models.PositiveIntegerField(default=1)
    difficulty = models.SmallIntegerField(choices=DIFFICULTY_CHOICES)
    votes = models.ManyToManyField(AUTH_USER_MODEL, related_name='voted_recipes', through='recipes.Vote')

    def __str__(self):
        """
        Return the string representation of the model
        """
        return self.title


