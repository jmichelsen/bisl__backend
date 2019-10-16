from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DetailView, DeleteView,
                                  ListView, UpdateView)

from recipes.models import Recipe
from recipes.filters import RecipeFilter

class RecipeCreateView(CreateView):
    """

    View to create a recipe
    """
    model = Recipe
    fields = ['user', 'title', 'description', 'servings', 'ingredients', 'preparation_time',
              'cook_time', 'difficulty']

    def get_success_url(self):
        return reverse_lazy('detail-single-recipe', kwargs={'pk': self.object.id})


class RecipeListView(ListView):
    """

    View that lists all recipes OR filters by Ingredient
    """
    model = Recipe
    context_object_name = 'recipe_list'
    ordering = ['-created_at']


class RecipeDetailView(DetailView):
    """

    View to detail a single recipe
    """
    model = Recipe

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredients'] = self.object.ingredients.all()
        return context


class RecipeUpdateView(UpdateView):
    """

    View to update a recipe
    """
    model = Recipe
    fields = ['title', 'description', 'servings', 'ingredients', 'preparation_time',
              'cook_time', 'difficulty']

    def get_success_url(self):
        return reverse_lazy('detail-single-recipe', kwargs={'pk': self.object.id})


class RecipeDeleteView(DeleteView):
    """

    View to delete a recipe
    """
    model = Recipe
    success_url = reverse_lazy('list-recipe')
