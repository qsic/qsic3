import os
import sys

from local.parse_env_file import parse

envvars = parse('env.sh')
for k, v in envvars.items():
    os.environ.update(envvars)

from .base import *

# sys.path.append('/Applications/PyCharm.app/pycharm-debug.egg')
#
# import pydevd
# pydevd.settrace('localhost', port=50235, stdoutToServer=True, stderrToServer=True)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'qsic',
        'USER': '',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
# Serve static locally
# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = rootjoin(PROJECT_ROOT, 'collected_static')
# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/%s/' % STATIC_DIR

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
# Serve media locally
# Absolute filesystem path to the directory that
# will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = rootjoin(PROJECT_ROOT, '%s' % MEDIA_DIR)
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/%s/' % MEDIA_DIR

print('Project Root set to:', PROJECT_ROOT)
print('Static Root set to:', STATIC_ROOT)
print('Static URL set to:', STATIC_URL)
print('Media Root set to:', MEDIA_ROOT)
print('Media URL set to:', MEDIA_URL)