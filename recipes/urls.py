from django.urls import path

from django_filters.views import FilterView

from recipes.views import (RecipeCreateView, RecipeDetailView, RecipeListView,
                           RecipeUpdateView, RecipeDeleteView)
from recipes.filters import RecipeFilter

urlpatterns = [
    path('search/', FilterView.as_view(filterset_class=RecipeFilter), name='filter-recipe'),
    path('list/', RecipeListView.as_view(), name='list-recipe'),
    path('create/', RecipeCreateView.as_view(), name='create-recipe'),
    path('update/<int:pk>/', RecipeUpdateView.as_view(), name='update-recipe'),
    path('delete/<int:pk>/', RecipeDeleteView.as_view(), name='delete-recipe'),
    path('detail/<int:pk>/', RecipeDetailView.as_view(), name='detail-single-recipe'),

]
