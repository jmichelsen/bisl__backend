from django.urls import re_path, path

from common.views import HealthCheck


common_patterns = [
    re_path(r'^health-check/$', HealthCheck.as_view(extra_context={'page_title': 'Health Check'}), name='health_check'),
]
