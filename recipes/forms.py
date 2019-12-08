from django import forms

# local
from .models import Recipe, Ingredient, Step, Tip


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = (
            'user',
            'users_who_made_this',
            'ingredients',
            'votes',
        )


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = (
            'name',
            'description',
            'quantity',
            'weight',
            'volume',
        )


class StepForm(forms.ModelForm):
    class Meta:
        model = Step
        exclude = (
            'recipe',
            'number',
            'completed'
        )
