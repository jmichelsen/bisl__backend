from datetime import timedelta

from django.test import TestCase
from django.contrib.auth.models import User


from recipes.models import Recipe
from comments.models import Comment


class CommentModel(TestCase):

    @classmethod
    def setUpTestData(cls):

        user = User.objects.create(username='test_user')

        test_recipe = Recipe.objects.create(
            title='test_title',
            ingredients='test_ingredients',
            preparation_process='test_prep',
            preparation_time=timedelta(minutes=20),
            number_of_portions=2,
            difficulty=1)

        Comment.objects.create(
            author=user,
            recipe=test_recipe,
            text='testing')

    def test_string(self):
        expected = 'test_user: testing...'
        actual = Comment.objects.get(id=1).__str__()
        self.assertEquals(expected, actual)

    def test_string_fail(self):
        expected = 'test_user: testing'
        actual = Comment.objects.get(id=1).__str__()
        self.assertFalse(expected, actual)
