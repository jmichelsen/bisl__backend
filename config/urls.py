"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from common.urls import common_patterns
from api.urls import api_patterns
from messaging.urls import messaging_patterns

from recipes.urls import recipe_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('common/', include((common_patterns, 'common'))),
    path('api/', include((api_patterns, 'api'))),
    path('accounts/', include('allauth.urls')),
    path('recipe/', include((recipe_patterns, 'recipes'))),
    path('messages/', include((messaging_patterns, 'messaging'))),

]



