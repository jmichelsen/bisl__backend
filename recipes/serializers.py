from measurement.measures import Weight
from rest_framework import serializers

from recipes.models import Recipe, Ingredient


class WeightField(serializers.Field):
    """
    Used to serialize the python-measurements Weight class
    """
    default_error_messages = {
        'incorrect_type': 'Incorrect type. Expected a tuple, but got {input_type}',
        'invalid_unit': '{attribute_error}',
    }

    def to_representation(self, value):
        """
        Return serialized Weight field

        :param value: incoming value of Weight field
        :type value: Weight
        :return: dict containing float value with unit notation
        :rtype: dict
        """
        return value.unit, value.value

    def to_internal_value(self, data):
        """
        Convert primitive serialized value back to python-measurements Weight object

        :param data: tuple of Weight object as (unit, value)
        :type data: tuple
        :return: Weight object containing value and unit of measure
        :rtype: Weight
        """
        if not isinstance(data, tuple):
            self.fail('incorrect_type', input_type=type(data).__name__)

        data = {data[0]: data[1]}
        try:
            return Weight(**data)
        except AttributeError as exception:
            self.fail('invalid_unit', attribute_error=exception)


class IngredientSerializer(serializers.ModelSerializer):
    """
    Serializes Ingredient model
    """
    weight = WeightField()

    class Meta:
        model = Ingredient
        fields = ('name', 'description', 'quantity', 'weight',)


class RecipeSerializer(serializers.ModelSerializer):
    """
    Serializes Recipe model with Ingredients ManyToMany serialized and nested
    """
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'user', 'title', 'description', 'ingredients', 'preparation_time',
            'cook_time', 'servings', 'max_servings', 'difficulty',
        )


class MultipliedRecipeSerializer(RecipeSerializer):
    @property
    def data(self):
        """
        Calculate multiplied ingredients for desired_yield and return data

        :return: modified data
        :rtype: dict
        """
        data = super().data
        if self.context.get('desired_yield') and data.get('ingredients'):
            desired_yield = self.context.get('desired_yield')
            multiplier = desired_yield / data['servings'] * 100.0
            new_ingredients = []
            for ingredient in data['ingredients']:
                ingredient['quantity'] = float(ingredient['quantity'] * multiplier / 100.0)
                ingredient['weight'] = (ingredient['weight'][0], ingredient['weight'][1] * multiplier / 100.0)
                new_ingredients.append(ingredient)
            data['ingredients'] = new_ingredients
            data['servings'] = desired_yield
            data['max_servings'] = desired_yield
        return data
