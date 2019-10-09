from django.urls import path

from recipes.views import (RecipeCreateView, RecipeDetailView, RecipeListView,
                           RecipeUpdateView, RecipeDeleteView)

urlpatterns = [
    path('list/', RecipeListView.as_view(), name='list-recipe'),
    path('create/', RecipeCreateView.as_view(), name='create-recipe'),
    path('update/<int:pk>/', RecipeUpdateView.as_view(), name='update-recipe'),
    path('delete/<int:pk>/', RecipeDeleteView.as_view(), name='delete-recipe'),
    path('detail/<int:pk>/', RecipeDetailView.as_view(), name='detail-single-recipe'),

]
