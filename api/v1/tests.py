from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from rest_framework.test import APITestCase
from rest_framework import status

from fixtureless.factory import create

from recipes.models import Recipe
from recipes.serializers import RecipeSerializer


class TestRecipeApi(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='test_user')
        self.recipe = create(Recipe, {'title': 'testing'})
        self.recipe_list_url = reverse_lazy('api:v1:recipe-list')
        self.recipe_detail_url = reverse_lazy('api:v1:recipe-detail', kwargs={'pk': self.recipe.pk})

    def test_recipe_list(self):
        """
        Verify GET returns Recipe list
        """
        response = self.client.get(self.recipe_list_url)
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Recipe.objects.count(), 1)
        self.assertEqual(Recipe.objects.get().title, 'testing')
        self.assertEqual(response.data, serializer.data)

    def test_create_recipe(self):
        """
        Verify POST creates a Recipe
        """
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
        response = self.client.post(self.recipe_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['servings'], 2)

    def test_recipe_detail(self):
        """
        Verify GET returns Recipe detail
        """
        response = self.client.get(self.recipe_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'testing')

    def test_recipe_update(self):
        """
        Verify PATCH updates our Recipe
        """
        response = self.client.patch(self.recipe_detail_url, {'title': 'new_test_title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'new_test_title')

    def test_recipe_delete(self):
        """
        Verify DELETE, deletes a Recipe
        """
        response = self.client.delete(self.recipe_detail_url)
        check_detail_view_is_404 = self.client.get(self.recipe_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(check_detail_view_is_404.status_code, status.HTTP_404_NOT_FOUND)




