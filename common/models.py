# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from common.mixins.model import TimestampMixin


class BaseModel(TimestampMixin, models.Model):
    """
    Base model for use throughout the code for any model that needs a timestamp
    """
    class Meta:
        abstract = True

