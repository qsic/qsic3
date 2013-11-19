"""
    A custom ContentFile for S3 uploads/downloads.
"""
import hashlib

from django.core.files.base import ContentFile

from .utils import b64_string


class S3ContentFile(ContentFile):
    """Represents a single file object in S3"""
    def __init__(self, content, name=None, mimetype=None):
        super().__init__(content, name)
        self.mimetype = mimetype

    def __str__(self):
        return self.name

    @property
    def size(self):
        return len(self.content)

    def md5hash(self):
        """Return MD5 hash string of data"""
        data = self.content
        if not isinstance(data, bytes):
            data = data.encode(settings.ENCODING)
        digest = hashlib.md5(data).digest()
        return b64_string(digest)

    def read(self, num_of_bytes=None):
        pass

    def write(self, content):
        pass

    def close(self):
        pass
