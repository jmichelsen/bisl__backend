from django.urls import path, include

from .v1.urls import v1_patterns


api_patterns = [
    path('v1/', include((v1_patterns, 'v1'))),  # Uses Django REST Framework ViewSets
]
