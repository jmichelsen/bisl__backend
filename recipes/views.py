from django.urls import reverse_lazy
from django.views.generic import (CreateView, DetailView, DeleteView,
                                  ListView, UpdateView)

from recipes.models import Recipe


class RecipeCreateView(CreateView):
    """

    View to create a recipe
    """
    model = Recipe
    fields = ['user', 'title', 'description', 'servings', 'ingredients', 'preparation_time',
              'cook_time', 'difficulty']

    success_url = reverse_lazy('list-recipe')


class RecipeListView(ListView):
    """

    View that lists all recipes
    """
    model = Recipe
    context_object_name = 'recipe_list'


class RecipeDetailView(DetailView):
    """

    View to detail a single recipe
    """
    model = Recipe


class RecipeUpdateView(UpdateView):
    """

    View to update a recipe
    """
    model = Recipe
    fields = ['title', 'description', 'servings', 'ingredients', 'preparation_time',
              'cook_time', 'difficulty']
    success_url = reverse_lazy('list-recipe')


class RecipeDeleteView(DeleteView):
    """

    View to delete a recipe
    """
    model = Recipe
    success_url = reverse_lazy('list-recipe')
