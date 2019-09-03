"""
Common views
"""
from django.http import JsonResponse
from django.views.generic import View
from django.views.generic.base import ContextMixin


class HealthCheck(ContextMixin, View):
    """
    Generic health check view for use for inf
    """

    @staticmethod
    def get(_):
        """
        Generic get method for providing a health check
        :param _: Unused request
        :return: A JSON response to indicate health
        """
        return JsonResponse({
            'success': True,
        })
