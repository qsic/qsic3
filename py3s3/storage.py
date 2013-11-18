from urllib.parse import urljoin

from django.conf import settings
from django.core.files import File
from django.core.files.storage import Storage

from py3s3.files import S3File


class S3Storage(Storage):
    """A custom storage implimentation for use with py3s3"""

    def __init__(self):
        self.base_dir = ''
        self.bucket = settings.AWS_STORAGE_BUCKET_NAME
        self.access_key = settings.AWS_ACCESS_KEY_ID
        self.secret_key = settings.AWS_SECRET_ACCESS_KEY

    def _open(self, name, mode='rb'):
        name = self._prepend_base_dir(name)
        file = S3File(self.bucket, name)
        status, data = file.get()
        if status in (200,):
            f = File(data)
            f.close()
            return f
        else:
            raise IOError('py3s3 GET error. Response status: %s' % status)

    def _save(self, name, data):
        data.open()
        name = self._prepend_base_dir(name)
        file = S3File(self.bucket,
                      name,
                      data=data.read(),
                      access_key=self.access_key,
                      secret_key=self.secret_key)
        status = file.put()
        if status not in (200,):
            raise IOError('py3s3 PUT error. Response status: %s' % status)
        return name

    def _prepend_base_dir(self, name):
        """Return file name (ie. path) with the base directory prepended"""
        base = self.base_dir
        if base[0] != '/':
            base = '/' + base
        if name[0] != '/':
            name = '/' + name
        return base + name