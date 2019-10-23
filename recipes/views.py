from django.urls import reverse_lazy
from django.views.generic import (CreateView, DetailView, DeleteView,
                                  ListView, UpdateView)

from recipes.models import Recipe


class RecipeCreateView(CreateView):
    """
    View to create a recipe
    """
    model = Recipe
    fields = ('user', 'title', 'description', 'servings', 'ingredients', 'preparation_time',
              'cook_time', 'difficulty', )

    def get_success_url(self):
        return reverse_lazy('recipes:detail', kwargs={'pk': self.object.pk})


class RecipeListView(ListView):
    """
    View that lists all recipes OR filters by Ingredient
    """
    model = Recipe


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
    fields = ('title', 'description', 'servings', 'ingredients', 'preparation_time',
              'cook_time', 'difficulty', )

    def get_success_url(self):
        return reverse_lazy('recipes:detail', kwargs={'pk': self.object.id})


class RecipeDeleteView(DeleteView):
    """
    View to delete a recipe
    """
    model = Recipe
    success_url = reverse_lazy('recipes:list')
