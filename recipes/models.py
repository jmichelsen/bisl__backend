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

    @cached_property
    def upvotes(self):
        """
        Return upvote count
        """
        votes = self.votes.through.objects.filter(recipe=self)
        return votes.filter(up=True).count() - votes.filter(up=False).count()

    @property
    def vote_objects(self):
        return self.votes.through.objects.filter(recipe=self)

    def upvote(self, user):
        """
        Toggle vote either up (True) or to neutral

        :param user: User casting the vote
        :type user: User
        :return: None
        """
        try:
            vote = self.vote_objects.get(user=user)
            if vote.up is True:
                vote.up = None
            else:
                vote.up = True
            vote.save()
        except Vote.DoesNotExist:
            Vote.objects.create(user=user, recipe=self, up=True)

    def downvote(self, user):
        """
        Toggle vote either down (False) or to neutral

        :param user: User casting the vote
        :type user: User
        :return: None
        """
        try:
            vote = self.vote_objects.get(user=user)
            if vote.up is False:
                vote.up = None
            else:
                vote.up = False
            vote.save()
        except Vote.DoesNotExist:
            Vote.objects.create(user=user, recipe=self, up=False)

    @cached_property
    def total_time_required(self):
        """
        Calculate and return total prep + cook time for the recipe

        :return: Total cook time
        :rtype: timedelta
        """
        return self.preparation_time + self.cook_time

    def custom_yield(self, desired_yield):
        """
        Multiple the ingredients for a custom

        :return: an ephemeral Recipe object with custom yield applied
        :rtype: Recipe instance
        """
        from recipes.serializers import MultipliedRecipeSerializer

        if not desired_yield:
            return self
        return MultipliedRecipeSerializer(self, context={'desired_yield': desired_yield}).data


class Ingredient(BaseModel):
    """
    A single ingredient in a recipe
    """
    name = models.CharField(max_length=50)
    description = models.TextField()
    quantity = models.FloatField(default=0.0, null=True)
    weight = MeasurementField(measurement=Weight, null=True, default=0)
    volume = MeasurementField(measurement=Volume, null=True, default=0)

    def __str__(self):
        return f'{self.quantity} {self.weight or self.volume} {self.description} {self.name}'


class Vote(BaseModel):
    """
    A Vote where up=True is an upvote, up=False is a downvote, and up=None is neutral
    """
    recipe = models.ForeignKey('recipes.Recipe', models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, models.CASCADE)
    up = models.BooleanField(null=True)


class Step(BaseModel):
    """
    A single step in a recipe
    """
    recipe = models.ForeignKey('recipes.Recipe', models.CASCADE, related_name='steps')
    name = models.CharField(max_length=100)
    number = models.PositiveSmallIntegerField()
    directions = models.TextField()
    completed = models.BooleanField(default=False)


class Tip(BaseModel):
    """
    Tips users have submitted to recipes
    """
    author = models.ForeignKey(AUTH_USER_MODEL, models.SET(get_system_user), related_name='tips')
    contents = models.TextField()


class Nutrition(BaseModel):
    """
    Nutrition facts for a recipe
    """
    calories = MeasurementField(measurement=Energy, default=0)
    total_fat = MeasurementField(measurement=Volume, default=0)
    saturated_fat = MeasurementField(measurement=Volume, default=0)
    cholesterol = MeasurementField(measurement=Volume, default=0)
    sodium = MeasurementField(measurement=Volume, default=0)
    potassium = MeasurementField(measurement=Volume, default=0)
    carbohydrates = MeasurementField(measurement=Volume, default=0)
    fiber = MeasurementField(measurement=Volume, default=0)
    sugar = MeasurementField(measurement=Volume, default=0)
    protein = MeasurementField(measurement=Volume, default=0)
    vitamin_a = models.FloatField(default=0.0)  # International Units
    vitamin_c = MeasurementField(measurement=Volume, default=0)
    calcium = MeasurementField(measurement=Volume, default=0)
    iron = MeasurementField(measurement=Volume, default=0)
    vitamin_d = models.FloatField(default=0.0)  # International Units
    vitamin_e = models.FloatField(default=0.0)  # International Units
    vitamin_k = MeasurementField(measurement=Volume, default=0)
    thiamin = MeasurementField(measurement=Volume, default=0)
    riboflavin = MeasurementField(measurement=Volume, default=0)
    niacin = MeasurementField(measurement=Volume, default=0)
    vitamin_b6 = MeasurementField(measurement=Volume, default=0)
    folate = MeasurementField(measurement=Volume, default=0)
    vitamin_b12 = MeasurementField(measurement=Volume, default=0)
    biotin = MeasurementField(measurement=Volume, default=0)
    pantothenic_acid = MeasurementField(measurement=Volume, default=0)
    phosphorus = MeasurementField(measurement=Volume, default=0)
    iodine = MeasurementField(measurement=Volume, default=0)
    magnesium = MeasurementField(measurement=Volume, default=0)
    zinc = MeasurementField(measurement=Volume, default=0)
    selenium = MeasurementField(measurement=Volume, default=0)
    copper = MeasurementField(measurement=Volume, default=0)
    manganese = MeasurementField(measurement=Volume, default=0)
    chromium = MeasurementField(measurement=Volume, default=0)
    molybdenum = MeasurementField(measurement=Volume, default=0)
    chloride = MeasurementField(measurement=Volume, default=0)


