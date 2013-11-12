"""
    A custom boto interface for S3 connections uploads/downloads.
"""

from base64 import b64encode
import hashlib

from datetime import datetime
import hmac
from http.client import HTTPConnection
from wsgiref.handlers import format_date_time

S3_URL = '%s.s3.amazon.com/'

class FileNameError(ValueError):
    pass


class S3File(object):
    """Represents a single file object in S3"""
    def __init__(self, name=None, data=None, mimetype=None,
                 bucket=None, access_key=None, secret_key=None):
        self._name = None
        self._data = None
        self._mimetype = None
        self._bucket = None
        self._access_key = None
        self._secret_key = None
        self.name  = name
        self.data = data
        self.mimetype = mimetype
        self.bucket = bucket
        self.access_key = access_key
        self.secret_key = secret_key

    @property
    def name(self):
        """Return file path relative to bucket as name"""
        return self._name

    @name.setter
    def name(self, name):
        if not name:
            raise FileNameError('Can not use %s as an S3 key name' % name)
        self._name = name

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def mimetype(self):
        return self._mimetype

    @mimetype.setter
    def mimetype(self, value):
        self._mimetype = value

    @property
    def bucket(self):
        return self._bucket

    @bucket.setter
    def bucket(self, value):
        """Apply bucket reqs"""
        self._bucket = value

    @property
    def access_key(self):
        return self._access_key

    @access_key.setter
    def access_key(self, value):
        self._access_key = value

    @property
    def secret_key(self):
        return self._secret_key

    @secret_key.setter
    def secret_key(self, value):
        self._secret_key = value

    def acl_dict(self):
        """Access Control List"""
        # TODO
        pass

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

        conn = HTTPConnection((S3_URL % self.bucket))
        conn.request('PUT', self.name, self.data, self._put_headers())

        # TODO urljoin here
        uri = 'http://' + (S3_URL % self.bucket) + self.name
        return (conn.getresponse(), uri)

    def get(self):
        """Download data from S3 into data buffer"""
        pass

    def _signature(self, timestamp):
        """
        Construct a signature by making an RFC2104 HMAC-SHA1
        of the following and converting it to Base64.

        HTTP-Verb + "\n" +
        [Content-MD5] + "\n" +
        [Content-Type] + "\n" +
        Date + "\n" +
        [CanonicalizedAmzHeaders +/n]
        [CanonicalizedResource]
        """
        params = [
            'PUT',
            self._md5hash(),
            self.mimetype,
            timestamp,
            'x-amz-acl:public-read',
            '/' + self.bucket + '/' + self.name
        ]
        params_string = '\n'.join(params)
        hmac_string = hmac.new(
            aws_secret.encode('utf-8'),
            params_string.encode('utf-8'),
            hashlib.sha1
        )
        signature = b64encode(hmac_string).digest().decode('utf-8')
        return signature

    def _md5hash(self):
        """Return MD5 hash of data"""
        #data = b64encode().('utf-8')
        md5 = hashlib.md5(data)
        return hashlib.md5(self.data).digest()

    def _put_headers(self):
        """Return dict of headers and values

        PUT /destinationObject HTTP/1.1
        Host: destinationBucket.s3.amazonaws.com
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
        headers = {}
        headers['Date'] = timestamp
        headers['Authorization'] = (''.join([
            'AWS' + ' ',
            self.access_key,
            ':',
            self._signature(timestamp)])
        )
        headers['Content-Length'] = len(self.data)
        # TODO md5 hash
        #headers['Content-MD5'] = self._md5hash()
        headers['Content-Type'] = self.mimetype
        headers['x-amz-acl'] = 'public-read'
        return headers

    def _get_headers(self):
        pass
