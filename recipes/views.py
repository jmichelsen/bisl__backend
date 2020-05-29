from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import (CreateView, DetailView, DeleteView,
                                  ListView, UpdateView, RedirectView)
from django.views.generic.edit import FormMixin

from recipes.mixins import AdminOrOwnerPermissionMixin
from recipes.models import Recipe

from comments.forms import CommentForm


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


class RecipeDetailView(FormMixin, DetailView):
    """
    View to detail a single recipe
    """
    model = Recipe
    form_class = CommentForm
    success_message = 'Comment submitted. Awaiting approval.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredients'] = self.object.ingredients.all()
        context['comments'] = self.object.comments.filter(active=True)
        context['form'] = self.get_form()
        return context

    # Add a post method for users to submit comments
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        form.instance.author = request.user
        if form.is_valid():
            messages.success(request, 'Comment submitted. Awaiting approval', extra_tags='admin_approval')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.recipe = self.object
        form.save()
        return HttpResponseRedirect(self.request.path_info)


class RecipeStarToggle(RedirectView):

    """
    Lets user give and remove a star to a recipe
    """

    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        recipe = get_object_or_404(Recipe, pk=pk)
        user = self.request.user
        if user.is_authenticated:
            if user in recipe.stars.all():
                recipe.stars.remove(user)
            else:
                recipe.stars.add(user)
        return reverse('recipes:detail', args=[recipe.pk])


class MyStarredRecipes(ListView):

    """
    View that shows a user their starred(favorite) recipes
    """

    model = Recipe

    def get_queryset(self):
        return Recipe.objects.filter(stars__username=self.request.user.username)


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

    def get_success_url(self):
        return reverse_lazy('recipes:detail', kwargs={'pk': self.object.pk})


class RecipeDeleteView(AdminOrOwnerPermissionMixin, DeleteView):
    """
    View to delete a recipe
    """
    permission_required = 'recipes.delete_recipe'
    model = Recipe
    success_url = reverse_lazy('recipes:list')
