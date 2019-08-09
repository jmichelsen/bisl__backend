from datetime import timedelta

from django.test import TestCase

from recipes.models import Recipe


class RecipeModelTest(TestCase):

    def setUp(self):
        self.obj1 = Recipe.objects.create(
            title='test_title',
            ingredients='test_ingredients',
            preparation_process='test_prep',
            preparation_time=timedelta(minutes=20),
            number_of_portions=2,
            difficulty=1)

    def test_title(self):
        self.assertEquals(self.obj1.title, 'test_title')

    def test_title_max_length(self):
        max_length = self.obj1._meta.get_field('title').max_length
        self.assertEquals(max_length, 100)

    def test_ingredients(self):
        self.assertEquals(self.obj1.ingredients, 'test_ingredients')

    def test_preparation_process(self):
        self.assertEquals(self.obj1.preparation_process, 'test_prep')

    def test_preparation_time(self):
        self.assertEquals(self.obj1.preparation_time, timedelta(minutes=20))

    def test_number_of_portions(self):
        self.assertEquals(self.obj1.number_of_portions, 2)

    def test_difficulty(self):
        self.assertEquals(self.obj1.difficulty, 1)

    def test_string(self):
        self.assertEquals(self.obj1.__str__(), self.obj1.title)
