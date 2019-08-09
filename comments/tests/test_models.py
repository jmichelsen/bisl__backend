from datetime import timedelta

from django.test import TestCase
from django.contrib.auth.models import User


from recipes.models import Recipe
from comments.models import Comment


class CommentModel(TestCase):

    def setUp(self):

        user = User.objects.create(username='test_user')

        self.obj1 = Recipe.objects.create(
            title='test_title',
            ingredients='test_ingredients',
            preparation_process='test_prep',
            preparation_time=timedelta(minutes=20),
            number_of_portions=2,
            difficulty=1
        )

        self.obj2 = Comment.objects.create(
            author=user,
            recipe=self.obj1,
            text='testing'
        )

    def test_author(self):
        self.assertEquals(self.obj2.author.username, 'test_user')

    def test_recipe(self):
        self.assertEquals(self.obj2.recipe.title, 'test_title')

    def test_text(self):
        self.assertEquals(self.obj2.text, 'testing')

    def test_ordering(self):
        ordering = self.obj2._meta.ordering
        self.assertEquals(ordering[0], '-created_at')

    def test_string(self):
        self.assertEquals(self.obj2.__str__(), 'test_user: testing...')


