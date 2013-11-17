"""
    A custom boto interface for S3 connections uploads/downloads.
"""

from base64 import b64encode
from contextlib import closing
from datetime import datetime
import hashlib
import hmac
from http.client import HTTPConnection
import urllib.parse
from wsgiref.handlers import format_date_time


S3_URL = '%s.s3.amazonaws.com'
ENCODING = 'utf-8'


def b64_string(bytestring):
    """Return an base64 encoded byte string as an ENCODING decoded string"""
    return b64encode(bytestring).decode(ENCODING)


class FileNameError(ValueError):
    pass


class S3File(object):
    """Represents a single file object in S3"""
    def __init__(self, bucket, name,
                 data=None, mimetype=None, access_key=None, secret_key=None):
        self.bucket = bucket
        self.name = name
        self.data = data
        self.mimetype = mimetype
        self.access_key = access_key
        self.secret_key = secret_key

    def _put_ready_check(self):
        """
        Check that all parameters needed for PUT operation are populated.
        """
        # TODO focus exceptions and messages
        if not self.name:
            raise Exception('No file name specified.')

        if not self.data:
            raise Exception('No data to upload.')

        if not self.bucket:
            raise Exception('No bucket specified for operation.')

        if not self.access_key:
            raise Exception('No access key id specified.')

        if not self.secret_key:
            raise Exception('No secret key specified.')

    def put(self):
        """Upload data to S3 at name equal to self._name"""
        self._put_ready_check()
        with closing(HTTPConnection(S3_URL % self.bucket)) as conn:
            conn.request('PUT',
                         self.name,
                         self.data,
                         headers=self._put_headers())
            return conn.getresponse().status

    def get(self):
        """
        Download data from S3 into data buffer as bytestring
        """
        with closing(HTTPConnection(S3_URL % self.bucket)) as conn:
            conn.request('GET',
                         self.name,
                         headers=self._get_headers())
            r = conn.getresponse()
            return r.status, r.read()

    def _put_signature(self, timestamp):
        """
        Construct a signature by making an RFC2104 HMAC-SHA1
        of the following and converting it to Base64 UTF-8 encoded string.

        HTTP-Verb + "\n" +
        [Content-MD5] + "\n" +
        [Content-Type] + "\n" +
        Date + "\n" +
        [CanonicalizedAmzHeaders +/n]
        [CanonicalizedResource]
        """
        mimetype = self.mimetype if self.mimetype else ''
        stringtosign = '\n'.join([
            'PUT',
            self._md5hash(),
            mimetype,
            timestamp,
            'x-amz-acl:public-read',
            '/' + self.bucket + self.name
        ])
        digest = hmac.new(
            self.secret_key.encode(ENCODING),
            stringtosign.encode(ENCODING),
            hashlib.sha1
        ).digest()
        return b64_string(digest)

    def _get_signature(self, timestamp):
        """
        Return a signature for use in GET requests
        """
        stringtosign = '\n'.join([
            'GET',
            '',
            '',
            timestamp,
            '/' + self.bucket + self.name
        ])
        digest = hmac.new(
            self.secret_key.encode(ENCODING),
            stringtosign.encode(ENCODING),
            hashlib.sha1
        ).digest()
        return b64_string(digest)

    def _md5hash(self):
        """Return MD5 hash string of data"""
        data = self.data.encode(ENCODING)
        digest = hashlib.md5(data).digest()
        return b64_string(digest)

    def _put_headers(self):
        """Return dict of headers and values

        Date: date
        Authorization: AWS AWSAccessKeyId:signature
        Content-Length: length
        Content-MD5: md5_digest
        Content-Type: type
        Content-Disposition: object_information
        Content-Encoding: encoding
        Cache-Control: caching
        Expires: expiration
        <request metadata>
        """
        timestamp = format_date_time(datetime.now().timestamp())
        headers = dict()
        headers['Date'] = timestamp
        headers['Authorization'] = (''.join([
            'AWS' + ' ',
            self.access_key,
            ':',
            self._put_signature(timestamp)])
        )
        headers['Content-Length'] = len(self.data)
        headers['Content-MD5'] = self._md5hash()
        if self.mimetype:
            headers['Content-Type'] = self.mimetype
        headers['x-amz-acl'] = 'public-read'
        return headers

    def _get_headers(self):
        """Return dict of headers and values for GET request"""
        timestamp = format_date_time(datetime.now().timestamp())
        headers = dict()
        headers['Date'] = timestamp
        if self.access_key and self.secret_key:
            headers['Authorization'] = ''.join([
                'AWS' + ' ',
                self.access_key,
                ':',
                self._get_signature(timestamp)])
        return headers
