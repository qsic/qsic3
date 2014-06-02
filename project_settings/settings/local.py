import sys

from .base import *

sys.path.append('/Users/paul/Code/python/py3s3')

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

SECRET_KEY = 'asdaaefaefaefaefefaefae'
