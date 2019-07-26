from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import re_path, path

from common.views import HealthCheck


info_dict = {
    # 'queryset': Entry.objects.all(),
    # 'date_field': 'pub_date',
}

common_patterns = [
    re_path(r'^health-check/$', HealthCheck.as_view(extra_context={'page_title': 'Health Check'}), name='health_check'),
]


# path('sitemap.xml', sitemap,
#      {'sitemaps': {'blog': GenericSitemap(info_dict, priority=0.6)}},
#      name='django.contrib.sitemaps.views.sitemap'),

# https://docs.djangoproject.com/en/2.0/ref/contrib/sitemaps/#django.contrib.sitemaps.GenericSitemap
