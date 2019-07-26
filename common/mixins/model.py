from django.db import models


class TimestampMixin(models.Model):
    """
    Model mixin to add timestamps to objects
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
