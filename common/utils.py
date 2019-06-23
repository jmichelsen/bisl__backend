import json
import os

from django.core.exceptions import ImproperlyConfigured
from django.template.loader import get_template


def get_env_variable(var_name, default=None):
    """
    Get the environment variable or return exception
    """
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        if os.environ.get('IN_DOCKER'):
            return str()
        message = 'Set the {} environment variable'.format(var_name)
        raise ImproperlyConfigured(message)


def set_env_from_secrets():
    """
    Take the secrets defined in docker-compose.yml and push them into the
    docker environment
    """
    try:
        with open('/run/secrets/SECRETS', 'r') as secrets:
            secrets_dict = json.load(secrets)
            for key, value in secrets_dict.items():
                try:
                    os.environ[key]
                except KeyError:
                    os.environ[key] = value
    except FileNotFoundError:
        pass


def render_to_template(template_name, context=None):
    if not context:
        context = dict()
    template = get_template(template_name)
    return template.render(context)
