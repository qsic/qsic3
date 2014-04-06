import os

from django.core.exceptions import ImproperlyConfigured


def get_env_var(env_var, default=None, isbool=False):
    """
    Return value of envirnoment variable or throw exception
    """
    try:
        env_value = os.environ.get(env_var, default)
        if isbool:
            env_value = 'true' in str(env_value).lower().strip()
        return env_value
    except KeyError:
        error_msg = '{} environment variable not set'.format(env_var)
        raise ImproperlyConfigured(error_msg)
