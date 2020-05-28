from django.contrib import admin

from .models import Recipe, Ingredient, Vote, Step, Nutrition, Tip

# Register your models here.

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Vote)
admin.site.register(Step)
admin.site.register(Nutrition)
admin.site.register(Tip)


