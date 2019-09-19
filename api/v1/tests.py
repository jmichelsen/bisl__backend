from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from rest_framework.test import APITestCase
from rest_framework import status

from fixtureless.factory import create

from recipes.models import Recipe


class TestRecipeApi(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='test_user')
        self.recipe = create(Recipe, {'title': 'testing'})

    def test_recipe_list(self):
        response = self.client.get(reverse_lazy('api:v1:recipe-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_account(self):
        url = reverse_lazy('api:v1:recipe-list')
        data = {
            "user": 1,
            "title": "testing",
            "description": "test description",
            "ingredients": [],
            "preparation_time": "00:00:01.500000",
            "cook_time": "00:00:03",
            "servings": 2,
            "max_servings": 3,
            "difficulty": 1
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_recipe_detail(self):
        response = self.client.get(reverse_lazy('api:v1:recipe-detail', kwargs={'pk': self.recipe.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'testing')

    def test_recipe_update(self):
        response = self.client.patch(reverse_lazy('api:v1:recipe-detail',
                                                  kwargs={'pk': self.recipe.pk}), {'title': 'new_test_title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_recipe_delete(self):
        response = self.client.delete(reverse_lazy('api:v1:recipe-detail', kwargs={'pk': self.recipe.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)




