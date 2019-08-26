from django.contrib.auth import get_user_model
from django.test import TestCase

from fixtureless.factory import create

from comments.models import Comment
from recipes.models import Recipe


class TestCommentModel(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='test_user')
        self.comment = create(Comment)
        self.recipe = create(Recipe)

    def test_comment_str(self):
        expected = Comment.__str__(self.comment)
        actual = self.comment.__str__()
        self.assertEqual(expected, actual)

