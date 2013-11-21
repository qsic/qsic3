"""
    A custom ContentFile for S3 uploads/downloads.
"""
import hashlib

from django.core.files.base import ContentFile

from .config import ENCODING
from .utils import b64_string


class S3ContentFile(ContentFile):
    """
    Represents a single file object in S3. Acts more like a data container
    at the moment.
    """
    def __init__(self, content, name=None, mimetype=None):
        super().__init__(content, name)
        self._content = None
        self.content = content
        self.mimetype = mimetype

    def __str__(self):
        return self.name

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        """
        Set content to byte string, encoding if necessary
        """
        if isinstance(value, bytes):
            self._content = value
        else:
            self._content = value.encode(ENCODING)

    def md5hash(self):
        """Return the MD5 hash string of the file content"""
        digest = hashlib.md5(self.content).digest()
        return b64_string(digest)

    def read(self, num_of_bytes=None):
        return self.content

    def write(self, content):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError
