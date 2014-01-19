# Django settings for qsic3 project.
import os

from django.core.exceptions import ImproperlyConfigured

import dj_database_url


def get_env_var(env_var, default=None, isbool=False):
    """
    Return value of envirnoment variable or throw exception
    """
    try:
        env_value = os.environ.get(env_var, default)
        if isbool:
            env_value = 'true' in str(env_value).lower()
        return env_value
    except KeyError:
        error_msg = '{} environment variable not set'.format(env_var)
        raise ImproperlyConfigured(error_msg)

DEBUG = get_env_var('DJANGO_DEBUG', default=False, isbool=True)
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG


# should point to qsic3 directory
def dirname(file, depth):
    """Return directory name containing file depth levels deep"""
    return os.path.dirname(dirname(file, depth-1)) if depth else file

PROJECT_ROOT = os.path.realpath(dirname(__file__, 3))
if DEBUG:
    print('Project Root set to:', PROJECT_ROOT)

ADMINS = (
    ('Leo Mendoza', 'leomendoza@gmail.com'),
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

SITE_ID = 2

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

SERVE_STATIC = get_env_var('DJANGO_SERVE_STATIC', default=False, isbool=True)
if SERVE_STATIC:
    # Serve static locally
    # Absolute path to the directory static files should be collected to.
    # Don't put anything in this directory yourself; store your static files
    # in apps' "static/" subdirectories and in STATICFILES_DIRS.
    # Example: "/home/media/media.lawrence.com/static/"
    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'collected_static')

    # URL prefix for static files.
    # Example: "http://media.lawrence.com/static/"
    STATIC_URL = '/%s/' % STATIC_DIR

else:
    # Serve static from AWS
    # tell django to use django-storages
    STATICFILES_STORAGE = 'py3s3.storage.S3StaticStorage'
    STATIC_ROOT = AWS_S3_BUCKET_URL + '/' + STATIC_DIR + '/'
    STATIC_URL = STATIC_ROOT

# ADMIN STATIC
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'


SERVE_MEDIA = get_env_var('DJANGO_SERVE_MEDIA', default=False, isbool=True)
if SERVE_MEDIA:
    # Serve media locally
    # Absolute filesystem path to the directory that
    # will hold user-uploaded files.
    # Example: "/home/media/media.lawrence.com/media/"
    MEDIA_ROOT = os.path.join(PROJECT_ROOT, '%s' % MEDIA_DIR)

    # URL that handles the media served from MEDIA_ROOT. Make sure to use a
    # trailing slash.
    # Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
    MEDIA_URL = '/%s/' % MEDIA_DIR

else:
    # Serve media from AWS
    # tell django to use django-storages
    # DEFAULT_FILE_STORAGE = lambda: S3BotoStorage(location=MEDIA_DIR)
    MEDIA_ROOT = AWS_S3_BUCKET_URL + '/' + MEDIA_DIR + '/'
    MEDIA_URL = MEDIA_ROOT
    DEFAULT_FILE_STORAGE = 'py3s3.storage.S3MediaStorage'

if SERVE_STATIC or SERVE_MEDIA:
    # Only upload new or changed files to AWS
    AWS_PRELOAD_METADATA = True

if DEBUG:
    print('Static Root set to:', STATIC_ROOT)
    print('Static URL set to:', STATIC_URL)
    print('Media Root set to:', MEDIA_ROOT)
    print('Media URL set to:', MEDIA_URL)

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.

    os.path.join(PROJECT_ROOT, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
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
    'south',
    # 'storages', no longer using storages 2013.11.03
    #'easy_thumbnails',
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

        'py3s3': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
