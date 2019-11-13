from django.contrib.auth import get_user_model
from django.test import TestCase
from datetime import timedelta

from recipes.models import Recipe


class TestRecipe(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create(username='user1')
        self.user2 = get_user_model().objects.create(username='user2')
        self.user3 = get_user_model().objects.create(username='user3')
        self.recipe1 = Recipe.objects.create(user=self.user1,
                                             title='test_title',
                                             preparation_time=timedelta(seconds=2400),
                                             cook_time=timedelta(seconds=2400),
                                             difficulty=2,)
        self.recipe1.cast_vote(self.user1, up=True)
        self.recipe1.cast_vote(self.user2, up=True)
        self.recipe1.cast_vote(self.user3, up=False)

    def test_str(self):
        """
        Validate the __str__ output is the Recipe.title value
        """
        expected = 'test_title'
        actual = Recipe.objects.get(title='test_title').__str__()
        self.assertEqual(expected, actual)

    def test_upvote_count(self):
        """
        Validate total number of upvotes for a recipe
        """
        expected = 2
        actual = self.recipe1.vote_objects.filter(up=True).count()
        self.assertEqual(expected, actual)

    def test_vote_objects(self):
        """
        Validate total number of votes for a recipe
        """
        expected = 3
        actual = len(self.recipe1.vote_objects)
        self.assertEqual(expected, actual)

    def test_cast_vote_none(self):
        """
        Change a user vote to None
        """
        self.recipe1.cast_vote(user=self.user1, up=None)
        expected = 1
        actual = self.recipe1.vote_objects.filter(up=True).count()
        self.assertEqual(expected, actual)

    def test_cast_vote_false(self):
        """
        Change a user vote to False
        """
        self.recipe1.cast_vote(user=self.user1, up=False)
        expected = 2
        actual = self.recipe1.vote_objects.filter(up=False).count()
        self.assertEqual(expected, actual)

    def test_cast_vote_true(self):
        """
        Change a user vote to True
        """
        self.recipe1.cast_vote(user=self.user1, up=True)
        expected = 2
        actual = self.recipe1.vote_objects.filter(up=True).count()
        self.assertEqual(expected, actual)

    def test_total_time_required(self):
        """
        Validate the total prep + cook time for the recipe
        """
        expected = 4800
        actual = Recipe.objects.get(title='test_title').total_time_required.seconds
        self.assertEqual(expected, actual)
