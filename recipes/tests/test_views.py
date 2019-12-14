from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import TestCase, Client
from django.urls import reverse
from fixtureless.factory import create

from recipes.models import Recipe


class TestRecipeViews(TestCase):

    def setUp(self):
        super().setUp()
        self.user1 = get_user_model().objects.create(username='test_user1')
        self.form = create(Recipe, {'user': self.user1, 'title': 'test_title'})
        self.client = Client()

        # group and permission setup
        self.group = Group(name='recipe admin')
        self.group.save()
        add_delete_permission = Permission.objects.get(name='Can delete recipe')
        add_edit_permission = Permission.objects.get(name='Can change recipe')

        self.user2 = get_user_model().objects.create(username='test_user')
        self.user2.groups.add(self.group)
        self.group.permissions.add(add_delete_permission, add_edit_permission)

    def test_create_recipe(self):
        """
        Test form instance uses self.user for posting recipes
        """
        self.client.force_login(user=self.user1)
        response = self.client.post(reverse('recipes:create'), {'title': self.form.title})
        self.assertEqual(Recipe.objects.first().user, self.form.user)
        self.assertContains(response, 'test_title')

    def test_logged_out_user(self):
        """
        Test logged out user can not create,  redirects user to login page
        """
        self.client.logout()
        response = self.client.get(reverse('recipes:create'))
        self.assertRedirects(response, '/accounts/login/?next=/recipe/create/')

    def test_display_recipe(self):
        response = self.client.get(reverse('recipes:detail', kwargs={'pk': self.form.pk}))
        self.assertContains(response, 'test_title')

    def test_update_recipe(self):
        """
        Test UpdateView updates users recipe
        """
        self.client.force_login(user=self.user1)
        response = self.client.put(reverse('recipes:update', kwargs={'pk': self.form.pk}),
                                   {'title': 'testing'})
        self.assertEqual(response.status_code, 200)

        # reloads a models value from the database
        self.form.refresh_from_db()
        self.assertEqual(self.form.title, 'test_title')

    def test_unauthorized_update_view(self):
        """
        Test UpdateView is forbidden to unauthorized users
        """
        self.client.force_login(user=get_user_model().objects.create(username='unauthorized_user'))
        response = self.client.get(reverse('recipes:update', kwargs={'pk': self.form.pk}))
        self.assertEqual(response.status_code, 403)

    def test_delete_confirm_page(self):
        """
        Test DeleteView takes user to confirmation page
        """
        self.client.force_login(user=self.user1)
        response = self.client.get(reverse('recipes:delete', kwargs={'pk': self.form.pk}))
        self.assertContains(response, 'delete')

    def test_delete_recipe(self):
        """
        Test DeleteView deletes a recipe
        """
        self.client.force_login(user=self.user1)
        response = self.client.post(reverse('recipes:delete', kwargs={'pk': self.form.pk}))
        self.assertRedirects(response, reverse('recipes:list'))
        self.assertFalse(Recipe.objects.filter(pk=self.form.pk).exists())

    def test_unauthorized_delete_view(self):
        """
        Test DeleteView is forbidden to unauthorized users
        """
        self.client.force_login(user=get_user_model().objects.create(username='unauthorized_user'))
        response = self.client.get(reverse('recipes:delete', kwargs={'pk': self.form.pk}))
        self.assertEqual(response.status_code, 403)

    def test_admin_can_delete_recipe(self):
        """
        Test recipe admin can delete recipe
        """
        self.client.force_login(user=self.user2)

        response = self.client.post(reverse('recipes:delete', kwargs={'pk': self.form.pk}))
        self.assertRedirects(response, reverse('recipes:list'))

    def test_admin_can_update_recipe(self):
        """
        Test recipe admin can update users recipe
        """
        self.client.force_login(user=self.user2)
        response = self.client.put(reverse('recipes:update', kwargs={'pk': self.form.pk}),
                                   {'title': 'testing123'})
        self.assertEqual(response.status_code, 200)

