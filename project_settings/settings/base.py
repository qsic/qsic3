# Django settings for qsic3 project.
import os

import dj_database_url
from easy_thumbnails.conf import Settings as thumbnail_settings


def get_env_var(env_var, default=None, isbool=False):
    """
    Return value of envirnoment variable or throw exception
    """
    from django.core.exceptions import ImproperlyConfigured
    try:
        env_value = os.environ.get(env_var, default)
        if isbool:
            env_value = 'true' in str(env_value).lower().strip()
        return env_value
    except KeyError:
        error_msg = '{} environment variable not set'.format(env_var)
        raise ImproperlyConfigured(error_msg)

# Return directory name containing file depth levels deep
dirname = lambda file, depth: os.path.dirname(dirname(file, depth-1)) if depth else file
PROJECT_ROOT = os.path.abspath(dirname(__file__, 3))
rootjoin = lambda *args: os.path.join(PROJECT_ROOT, *args)

DEBUG = get_env_var('DJANGO_DEBUG', default=False, isbool=True)
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG

ADMINS = (
    ('Paul Logston', 'code@logston.me'),
)

MANAGERS = ADMINS

DATABASE_URL = get_env_var('DATABASE_URL')
DATABASES = {
    'default': dj_database_url.config()
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Filesystem directory names for static and media files
STATIC_DIR = 'static'
MEDIA_DIR = 'media'

# AWS file access info
AWS_ACCESS_KEY_ID = get_env_var('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_env_var('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = get_env_var('AWS_STORAGE_BUCKET_NAME')

# Of the format: '//bucket_name.s3.amazonaws.com/[media|static]/'
AWS_S3_BUCKET_URL = '//%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# Encoding for AWS transactions
ENCODING = 'utf-8'

# Serve static from AWS
# tell django to use django-storages
STATICFILES_STORAGE = 'django_py3s3.storages.S3StaticStorage'
STATIC_ROOT = AWS_S3_BUCKET_URL + '/' + STATIC_DIR + '/'
STATIC_URL = STATIC_ROOT

# Serve media from AWS
MEDIA_ROOT = AWS_S3_BUCKET_URL + '/' + MEDIA_DIR + '/'
MEDIA_URL = MEDIA_ROOT
DEFAULT_FILE_STORAGE = 'django_py3s3.storages.S3MediaStorage'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    rootjoin('static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'project_settings.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'project_settings.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'django_extensions',
    'easy_thumbnails',
    'image_cropping',
    'qsic',
    'py3s3',
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# Make this unique, and don't share it with anybody.
SECRET_KEY = get_env_var('DJANGO_SECRET_KEY')

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },

    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d '
                      '%(thread)d %(message)s'
        },

        'medium': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },

        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },

    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },

        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'medium'
        }
    },

    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },

        'qsic': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}


# easy_thumbnails and django image cropping
THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnail_settings.THUMBNAIL_PROCESSORS

#THUMBNAIL_DEFAULT_STORAGE = 'easy_thumbnails.storage.ThumbnailFileSystemStorage'
THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE

IMAGE_CROPPING_SIZE_WARNING = True

SOUTH_MIGRATION_MODULES = {
    'easy_thumbnails': 'easy_thumbnails.south_migrations',
}
