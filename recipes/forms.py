from django import forms

# local
from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ('user', 'users_who_made_this', 'ingredients', 'votes')
