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

    def test_string(self):
        expected = 'test_title'
        actual = Recipe.objects.get(title='test_title').__str__()
        self.assertEquals(expected, actual)

     def test_title_max_length(self):
        max_length = Recipe._meta.get_field('title').max_length
        self.assertEquals(max_length, 100)

    def test_ingredients_max_length(self):
        max_length = Recipe._meta.get_field('ingredients').max_length
        self.assertEquals(max_length, 2000)
