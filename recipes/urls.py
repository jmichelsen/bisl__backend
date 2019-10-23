from django.urls import path

from django_filters.views import FilterView

from recipes.views import (RecipeCreateView, RecipeDetailView, RecipeListView,
                           RecipeUpdateView, RecipeDeleteView)
from recipes.filters import RecipeFilter

recipe_patterns = [
    path('search/', FilterView.as_view(filterset_class=RecipeFilter), name='filter'),
    path('list/', RecipeListView.as_view(), name='list'),
    path('create/', RecipeCreateView.as_view(), name='create'),
    path('update/<int:pk>/', RecipeUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', RecipeDeleteView.as_view(), name='delete'),
    path('detail/<int:pk>/', RecipeDetailView.as_view(), name='detail'),

]
