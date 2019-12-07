from datetime import timedelta
from django.test import TestCase

# local
from recipes.forms import RecipeForm
from recipes.models import Recipe


class TestRecipeFrom(TestCase):
    def test_valid_form(self):
        r = Recipe(
            title='test recipe',
            description='test recipe description',
            preparation_time=timedelta(microseconds=1),
            cook_time=timedelta(microseconds=1),
            servings=2,
            max_servings=3,
            difficulty=1,
        )
        form_data = {
            'title': r.title,
            'description': r.description,
            'preparation_time': r.preparation_time,
            'cook_time': r.cook_time,
            'servings': r.servings,
            'max_servings': r.max_servings,
            'difficulty': r.difficulty,
        }
        form = RecipeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        r = Recipe(
            title='',
            description='',
            preparation_time=timedelta(microseconds=1),
            cook_time=timedelta(microseconds=1),
            servings=2,
            max_servings=3,
            difficulty=1,
        )
        form_data = {
            'title': r.title,
            'description': r.description,
            'preparation_time': r.preparation_time,
            'cook_time': r.cook_time,
            'servings': r.servings,
            'max_servings': r.max_servings,
            'difficulty': r.difficulty,
        }
        form = RecipeForm(data=form_data)
        self.assertTrue(form.is_valid())

