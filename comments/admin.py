from django.contrib import admin

from .models import Comment

# Register your models here.


class CommentAdmin(admin.ModelAdmin):
    list_display = ('username', 'recipe', 'text', 'created_at', 'active')
    list_filter = ('active', 'created_at')
    search_fields = ('author__username', 'recipe__title', 'text')

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

    def username(self, obj):
        return obj.author.username


admin.site.register(Comment, CommentAdmin)

