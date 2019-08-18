from django.test import TestCase
from fixtureless.factory import create
from measurement.measures import Weight
from rest_framework.exceptions import ValidationError

from common.utils import get_system_user
from recipes.models import Ingredient, Recipe
from recipes.serializers import (
    MultipliedRecipeSerializer, RecipeSerializer,
    WeightField,
)


class TestWeightField(TestCase):
    def setUp(self):
        self.weight = Weight(g=1.5)

    def test_to_representation(self):
        """
        Verify Weight object is converted to tuple of (unit, value)
        """
        representation = WeightField().to_representation(self.weight)
        self.assertIsInstance(representation, tuple)
        self.assertEqual(representation[0], self.weight.unit)
        self.assertEqual(representation[1], self.weight.value)

    def test_to_internal_value__success(self):
        """
        Verify tuple of Weight object data can be converted successfully to Weight object
        """
        data = (self.weight.unit, self.weight.value)
        internal_value = WeightField().to_internal_value(data)
        self.assertIsInstance(internal_value, Weight)
        self.assertEqual(internal_value.unit, data[0])
        self.assertEqual(internal_value.value, data[1])

    def test_to_internal_value__incorrect_type(self):
        """
        Verify that ValidationError is raised for incorrect data type
        """
        with self.assertRaises(ValidationError):
            WeightField().to_internal_value('1.5, g')

    def test_to_internal_value__invalid_unit(self):
        """
        Verify that ValidationError is raised for invalid units of measure
        """
        with self.assertRaises(ValidationError):
            WeightField().to_internal_value(data=('gargantuan', 1.5))


class TestMultipliedRecipeSerializer(TestCase):
    def setUp(self):
        self.maxDiff = None
        user = get_system_user()
        self.recipe = create(Recipe, {'user': user, 'servings': 4})
        self.recipe.ingredients.add(create(Ingredient, {'quantity': 2, 'weight': 5}))

    def test_recipe_serialization__no_desired_yield(self):
        """
        Verify that MultipliedRecipe without a multiplier passed in is the same as a standard serialized Recipe
        """
        multiplied_data = MultipliedRecipeSerializer(self.recipe).data
        recipe_data = RecipeSerializer(self.recipe).data
        self.assertCountEqual(multiplied_data, recipe_data)

    def test_recipe_serialization__no_ingredients(self):
        """
        Verify that MultipliedRecipe without ingredients is the same as a standard serialized Recipe
        """
        self.recipe.ingredients.clear()
        multiplied_data = MultipliedRecipeSerializer(self.recipe, context={'desired_yield': 8}).data
        recipe_data = RecipeSerializer(self.recipe).data
        self.assertCountEqual(multiplied_data, recipe_data)

    def test_recipe_serialization__desired_yield_increase(self):
        """
        Verify that MultipliedRecipe with increased desired_yield is multiplied properly
        """
        multiplied_data = MultipliedRecipeSerializer(self.recipe, context={'desired_yield': 8}).data
        self.assertEqual(multiplied_data['ingredients'][0]['quantity'], 4)
        self.assertEqual(multiplied_data['ingredients'][0]['weight'][1], 10)

        multiplied_data = MultipliedRecipeSerializer(self.recipe, context={'desired_yield': 12}).data
        self.assertEqual(multiplied_data['ingredients'][0]['quantity'], 6)
        self.assertEqual(multiplied_data['ingredients'][0]['weight'][1], 15)

    def test_recipe_serialization__desired_yield_decrease(self):
        """
        Verify that MultipliedRecipe with reduced desired_yield is multiplied properly
        """
        multiplied_data = MultipliedRecipeSerializer(self.recipe, context={'desired_yield': 2}).data
        self.assertEqual(multiplied_data['ingredients'][0]['quantity'], 1)
        self.assertEqual(multiplied_data['ingredients'][0]['weight'][1], 2.5)

        multiplied_data = MultipliedRecipeSerializer(self.recipe, context={'desired_yield': 1}).data
        self.assertEqual(multiplied_data['ingredients'][0]['quantity'], .5)
        self.assertEqual(multiplied_data['ingredients'][0]['weight'][1], 1.25)
