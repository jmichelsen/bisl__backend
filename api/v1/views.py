"""
Views for the Recipe API
"""
from rest_framework import viewsets
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
