from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DetailView, DeleteView,
                                  ListView, UpdateView)

from recipes.mixins import AdminOrOwnerPermissionMixin
from recipes.models import Recipe


class RecipeCreateView(LoginRequiredMixin, CreateView):
    """
    View to create a recipe
    """
    model = Recipe
    fields = ('title', 'description', 'servings', 'ingredients', 'preparation_time',
              'cook_time', 'difficulty', )

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

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


class RecipeUpdateView(AdminOrOwnerPermissionMixin, UpdateView):
    """
    View to delete a recipe
    """
    permission_required = 'recipes.change_recipe'
    model = Recipe
    fields = ('title', 'description', 'servings', 'ingredients', 'preparation_time',
              'cook_time', 'difficulty', )

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('recipes:detail', kwargs={'pk': self.object.pk})


class RecipeDeleteView(AdminOrOwnerPermissionMixin, DeleteView):
    """
    View to delete a recipe
    """
    permission_required = 'recipes.delete_recipe'
    model = Recipe
    success_url = reverse_lazy('recipes:list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)



