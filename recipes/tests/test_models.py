from django.contrib.auth import get_user_model
from django.test import TestCase
from fixtureless.factory import create

from recipes.models import Recipe


class RecipeTestCase(TestCase):
    def setUp(self):
        get_user_model().objects.create(username='test_user')
        create(Recipe, {'title': 'test_title'})

    def test_str(self):
        """
        Validate the __str__ output is the Recipe.title value
        """
        expected = 'test_title'
        actual = Recipe.objects.get(title='test_title').__str__()
        self.assertEqual(expected, actual)
