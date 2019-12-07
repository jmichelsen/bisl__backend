from django.contrib.auth import get_user_model
from django.test import TestCase
from fixtureless.factory import create

# local
from comments.forms import CommentForm
from comments.models import Comment
from recipes.models import Recipe


class TestCommentForm(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='test_user')
        self.recipe = create(Recipe)

    def test_valid_form(self):
        """
        Validate a valid form
        """
        c = create(Comment)
        form_data = {'text': c.text}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """
        Validate an invalid form
        """
        form_data = {'text': ''}
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())
