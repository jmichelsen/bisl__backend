from datetime import timedelta

from django.test import TestCase

from recipes.models import Recipe


class RecipeTestCase(TestCase):
    def setUp(self):
        Recipe.objects.create(
            title='test_title',
            ingredients='test_ingredients',
            preparation_process='test_prep',
            preparation_time=timedelta(minutes=20),
            number_of_portions=2,
            difficulty=1)

    def test_str(self):
        """
        Validate the __str__ output is the Recipe.title value
        """
        expected = 'test_title'
        actual = Recipe.objects.get(title='test_title').__str__()
        self.assertEqual(expected, actual)
