from datetime import timedelta
from django.test import TestCase
from fixtureless.factory import create

# third-party
from measurement.measures import Volume, Weight

# local
from recipes.forms import RecipeForm, IngredientForm, StepForm
from recipes.models import Recipe, Ingredient, Step


class TestRecipeFrom(TestCase):
    def test_valid_form(self):
        """
        Validate a valid form
        """
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
        """
        Validate an invalid form
        """
        r = Recipe(
            title='',
            description='',
            preparation_time=None,
            cook_time=None,
            servings=None,
            max_servings=None,
            difficulty=None,
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
        self.assertFalse(form.is_valid())


class TestIngredientForm(TestCase):
    def test_valid_form(self):
        """
        Validate a valid form
        """
        i = Ingredient.objects.create(
            name='test_name',
            description='test_description',
            quantity=1.0,
            weight=Weight(kg=1),
            volume=Volume(us_pint=1),
        )
        form_data = {
            'name': i.name,
            'description': i.description,
            'quantity': i.quantity,
            'weight': i.weight,
            'volume': i.volume,
        }
        form = IngredientForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """
        Validate an invalid form
        """
        form_data = {
            'name': '',
            'description': '',
            'quantity': None,
            'weight': None,
            'volume': None,
        }
        form = IngredientForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestStepForm(TestCase):
    def test_valid_form(self):
        """
        Validate a valid form
        """
        s = create(Step)
        form_data = {'name': s.name, 'directions': s.directions}
        form = StepForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """
        Validate an invalid form
        """
        form_data = {'name': '', 'directions': ''}
        form = StepForm(data=form_data)
        self.assertFalse(form.is_valid())