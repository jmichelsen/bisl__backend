from django.test import TestCase
from django.contrib.auth.models import User

from fixtureless.factory import create

from recipes.models import Recipe
from comments.models import Comment


class TestCommentModel(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.comment = create(Comment)
        self.recipe = create(Recipe)

    def test_comment_str(self):
        expected = Comment.__str__(self.comment)
        actual = self.comment.__str__()
        self.assertEqual(expected, actual)

