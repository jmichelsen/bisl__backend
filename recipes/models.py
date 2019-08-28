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

    def cast_vote(self, user, up=None):
        """
        Toggle vote either down (False) or to neutral

        :param user: User casting the vote
        :type user: User
        :param up: the value of the vote; True, False, or None
        :type: bool
        :return: None
        """
        Vote.objects.update_or_create(user=user, recipe=self, up=up)

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

        :return: new serialized recipe object with the custom yield calculated into it
        :rtype: json
        """
        # imported here to avoid circular import
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

    class Meta:
        unique_together = ('user', 'recipe')


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
    recipe = models.OneToOneField('recipes.Recipe', models.CASCADE, null=True)
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


RECOMMENDED_DAILY_VALUE = Nutrition(
    calories=Energy(calorie=2000),
    total_fat=Weight(gram=65),
    saturated_fat=Weight(gram=20),
    cholesterol=Weight(milligram=300),
    sodium=Weight(milligram=2400),
    potassium=Weight(milligram=3500),
    carbohydrates=Weight(gram=300),
    fiber=Weight(gram=25),
    sugar=Weight(gram=24),
    protein=Weight(gram=50),
    vitamin_a=5000,
    vitamin_c=Weight(milligram=60),
    calcium=Weight(milligram=1000),
    iron=Weight(milligram=18),
    vitamin_d=400,
    vitamin_e=30,
    vitamin_k=Weight(microgram=80),
    thiamin=Weight(milligram=1.5),
    riboflavin=Weight(milligram=1.7),
    niacin=Weight(milligram=20),
    vitamin_b6=Weight(milligram=2.0),
    folate=Weight(microgram=400),
    vitamin_b12=Weight(microgram=6.0),
    biotin=Weight(microgram=300),
    pantothenic_acid=Weight(milligram=10),
    phosphorus=Weight(milligram=1000),
    iodine=Weight(microgram=150),
    magnesium=Weight(milligram=400),
    zinc=Weight(milligram=15),
    selenium=Weight(microgram=70),
    copper=Weight(milligram=2.0),
    manganese=Weight(milligram=2.0),
    chromium=Weight(microgram=120),
    molybdenum=Weight(microgram=75),
    chloride=Weight(milligram=3400)
)
