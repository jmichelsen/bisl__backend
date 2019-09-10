from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'recipes', views.RecipeViewSet)

v1_patterns = [
    path('', include(router.urls)),
]
