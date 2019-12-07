from django.test import TestCase

# local
from comments.forms import CommentForm
from comments.models import Comment


class TestCommentForm(TestCase):
    def test_valid_form(self):
        c = Comment.objects.create(text='test text',)
        form_data = {'text': c.text}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        c = Comment.objects.create(text='')
        form_data = {'text': c.text}
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())
