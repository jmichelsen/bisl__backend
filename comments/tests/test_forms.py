from django.test import TestCase
from comments.forms import CommentForm


class TestCommentForm(TestCase):
    def test_valid_form(self):
        form_data = {'text': 'text'}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())
