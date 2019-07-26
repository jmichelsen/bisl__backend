from django.db import models
from common.mixins.model import TimestampMixin
from django.contrib.auth.models import User

# Create your models here.

class Comment(TimestampMixin, models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey('recipes.Recipe', on_delete=models.CASCADE)
    text = models.TextField(max_length=2000)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'comments'

    def __str__(self):
        return f"{self.author}: {self.text[:50]}"