import django_filters

from recipes.models import Recipe


class RecipeFilter(django_filters.FilterSet):
    """
    Allow users to search by EXACT ingredient
    """

    class Meta:
        model = Recipe
        fields = ['ingredients__name']

