"""
    A custom Storage interface for storing files to S3.
"""
from contextlib import closing
from datetime import datetime
import hashlib
import hmac
from http.client import HTTPConnection
import urllib.parse
from wsgiref.handlers import format_date_time

from django.core.files.storage import Storage

from .config import BUCKET
from .config import AWS_ACCESS_KEY
from .config import AWS_SECRET_KEY
from .config import ENCODING
from .files import S3ContentFile
from .utils import b64_string

NETLOC = '%s.s3.amazonaws.com' % BUCKET


class S3Storage(Storage):
    """A custom storage implimentation for use with py3s3"""
    def __init__(self, name_prefix='', bucket=BUCKET,
                 access_key=AWS_ACCESS_KEY, secret_key=AWS_SECRET_KEY):
        self.name_prefix = name_prefix
        self.bucket = bucket
        self.access_key = access_key
        self.secret_key = secret_key

    @staticmethod
    def request_timestamp():
        return format_date_time(datetime.now().timestamp())

    def _prepend_name_prefix(self, name):
        """Return file name (ie. path) with the prefix directory prepended"""
        if not self.name_prefix:
            return name
        base = self.name_prefix
        if base[0] != '/':
            base = '/' + base
        if name[0] != '/':
            name = '/' + name
        return base + name

    def request_signature(self, stringtosign):
        """
        Construct a signature by making an RFC2104 HMAC-SHA1
        of the following and converting it to Base64 UTF-8 encoded string.
        """
        digest = hmac.new(
            self.secret_key.encode(ENCODING),
            stringtosign.encode(ENCODING),
            hashlib.sha1
        ).digest()
        return b64_string(digest)

    def _put_file(self, file_object):
        timestamp = self.request_timestamp()

        mimetype = file_object.mimetype if file_object.mimetype else ''
        stringtosign = '\n'.join([
            'PUT',
            file_object.md5hash(),
            mimetype,
            timestamp,
            'x-amz-acl:public-read',
            '/' + self.bucket + file_object.name
        ])
        signature = self.request_signature(stringtosign)

        headers = dict()
        headers['Date'] = timestamp
        headers['Authorization'] = ''.join(['AWS' + ' ',
                                            self.access_key,
                                            ':',
                                            signature])
        headers['Content-Length'] = file_object.size
        headers['Content-MD5'] = file_object.md5hash()
        if mimetype:
            headers['Content-Type'] = self.mimetype
        headers['x-amz-acl'] = 'public-read'

        with closing(HTTPConnection(NETLOC)) as conn:
            conn.request('PUT',
                         file_object.name,
                         file_object.read(),
                         headers=headers)
            response = conn.getresponse()

        if response.status not in (200,):
            raise IOError('py3s3 PUT error. Response status: %s' %
                          response.status)

    def _save(self, name, file_object):
        prefixed_name = self._prepend_name_prefix(name)
        file_object.name = prefixed_name
        self._put_file(file_object)
        return name

    def _get_file(self, name):
        """
        Return a signature for use in GET requests
        """
        timestamp = self.request_timestamp()
        stringtosign = '\n'.join([
            'GET',
            '',
            '',
            timestamp,
            '/' + self.bucket + self.name
        ])
        signature = self.request_signature(stringtosign)

        headers = dict()
        headers['Date'] = timestamp
        if self.access_key and self.secret_key:
            headers['Authorization'] = ''.join(['AWS' + ' ',
                                                self.access_key,
                                                ':',
                                                signature])
        with closing(HTTPConnection(NETLOC)) as conn:
            conn.request('GET',
                         name,
                         headers=headers)
            r = conn.getresponse()

        if not r.status in (200,):
            raise IOError('py3s3 GET error. Response status: %s' % r.status)

        return S3ContentFile(r.read())

    def _open(self, name, mode='rb'):
        prefixed_name = self._prepend_name_prefix(name)
        file = self._get_file(prefixed_name)
        file.name = name
        return file

    def delete(self, name):
        pass

    def exists(self, name):
        with closing(HTTPConnection(NETLOC)) as conn:
            conn.request('HEAD', self.url(name))
            return conn.getresponse().status == 200

    def listdir(self, path):
        pass

    def size(self, name):
        pass

    def url(self, name):
        scheme = 'http'
        netloc = NETLOC
        path = self._prepend_name_prefix(name)
        query = ''
        fragment = ''
        url_tuple = (scheme, netloc, path, query, fragment)
        return urllib.parse.urlunsplit(url_tuple)

    def modified_time(self, name):
        pass


class StaticS3Storage(S3Storage):
    def __init__(self):
        super().__init__()
        self.name_prefix = 'static/'


class MediaS3Storage(S3Storage):
    def __init__(self):
        super().__init__()
        self.name_prefix = 'media/'
