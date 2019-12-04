from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from fixtureless.factory import create

from recipes.models import Recipe


class TestRecipeViews(TestCase):

    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create(username='test_user')
        self.form = create(Recipe, {'title': 'test_title'})

    def test_create_recipe(self):
        """
        Test form instance uses self.user for posting recipes
        """
        self.client.post(reverse('recipes:create'), {'title': self.form.title})
        self.assertEqual(Recipe.objects.first().user, self.form.user)

    def test_logged_out_user(self):
        """
        Test logged out user can not create,  redirects user to login page
        """
        self.client = Client()
        self.client.logout()
        response = self.client.get(reverse('recipes:create'))
        self.assertRedirects(response, '/accounts/login/?next=/recipe/create/')

    def test_display_recipe(self):
        response = self.client.get(reverse('recipes:detail', kwargs={'pk': self.form.pk}))
        self.assertContains(response, 'test_title')

    def test_update_recipe(self):
        response = self.client.post(reverse('recipes:update', kwargs={'pk': self.form.pk}),
                                    {'title': 'testing'})
        self.assertEqual(response.status_code, 302)

        # reloads a models value from the database
        self.form.refresh_from_db()
        self.assertEqual(self.form.title, 'test_title')

    def test_unauthorized_update_view(self):
        """
        UpdateView is forbidden to unauthorized users
        """
        self.client.force_login(user=get_user_model().objects.create(username='unauthorized_user'))
        response = self.client.get(reverse('recipes:update', kwargs={'pk': self.form.pk}))
        self.assertEqual(response.status_code, 403)

    def test_delete_confirm_page(self):
        """
        DeleteView takes user to confirmation page
        """
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('recipes:delete', kwargs={'pk': self.form.pk}))
        self.assertContains(response, 'delete')

    def test_delete_recipe(self):
        """
        DeleteView deletes a recipe
        """
        self.client.force_login(user=self.user)
        response = self.client.post(reverse('recipes:delete', kwargs={'pk': self.form.pk}))
        self.assertRedirects(response, reverse('recipes:list'))
        self.assertFalse(Recipe.objects.filter(pk=self.form.pk).exists())

    def test_unauthorized_delete_view(self):
        """
        DeleteView is forbidden to unauthorized users
        """
        self.client.force_login(user=get_user_model().objects.create(username='unauthorized_user'))
        response = self.client.get(reverse('recipes:delete', kwargs={'pk': self.form.pk}))
        self.assertEqual(response.status_code, 403)
