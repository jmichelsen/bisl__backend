# Django
from django.conf import settings
from django.db import models

from common.models import BaseModel


class Comment(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe = models.ForeignKey('recipes.Recipe', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author}: {self.text[:50]}..."
