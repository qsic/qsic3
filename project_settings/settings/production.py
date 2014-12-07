from .base import *

# Set your DSN value
RAVEN_CONFIG = {
    'dsn': 'https://e92ff3ac19cd4d89945f1b5e428f061d:accc3dfff4044ffa9193e79a564c9175@app.getsentry.com/34299',
}

# Add raven to the list of installed apps
INSTALLED_APPS = INSTALLED_APPS + (
    # ...
    'raven.contrib.django.raven_compat',
)