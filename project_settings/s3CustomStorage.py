"""
    Custom AWS S3 Storage backend for Django 1.5 on Python 3.3.

    This is meant to be an interm solution until boto3 arrives and
    django-storages accomidates boto3.

    Based off of django-storages and boto.

    @author Paul Logston
"""

from django.conf import settings
from django.core.files.base import File
from django.core.files.storage import Storage


def setting(name, default=None):
    """
    Helper function to get a Django setting by name or (optionally) return
    a default (or else ``None``).
    """
    return getattr(settings, name, default)

class S3BotoStorage(Storage):
    """
    Amazon Simple Storage Service using Boto

    This storage backend supports opening files in read or write
    mode and supports streaming(buffering) data in chunks to S3
    when writing.
    """
    connection_class = S3Connection
    connection_response_error = S3ResponseError
    file_class = S3BotoStorageFile
    key_class = S3Key

    # used for looking up the access and secret key from env vars
    access_key_names = ['AWS_ACCESS_KEY_ID']
    secret_key_names = ['AWS_SECRET_ACCESS_KEY']

    access_key = setting('AWS_ACCESS_KEY_ID')
    secret_key = setting('AWS_SECRET_ACCESS_KEY')
    file_overwrite = setting('AWS_S3_FILE_OVERWRITE', True)
    headers = setting('AWS_HEADERS', {})
    bucket_name = setting('AWS_STORAGE_BUCKET_NAME')
    auto_create_bucket = setting('AWS_AUTO_CREATE_BUCKET', False)
    default_acl = setting('AWS_DEFAULT_ACL', 'public-read')
    bucket_acl = setting('AWS_BUCKET_ACL', default_acl)
    querystring_auth = setting('AWS_QUERYSTRING_AUTH', True)
    querystring_expire = setting('AWS_QUERYSTRING_EXPIRE', 3600)
    reduced_redundancy = setting('AWS_REDUCED_REDUNDANCY', False)
    location = setting('AWS_LOCATION', '')
    encryption = setting('AWS_S3_ENCRYPTION', False)
    custom_domain = setting('AWS_S3_CUSTOM_DOMAIN')
    calling_format = setting('AWS_S3_CALLING_FORMAT', SubdomainCallingFormat())
    secure_urls = setting('AWS_S3_SECURE_URLS', True)
    file_name_charset = setting('AWS_S3_FILE_NAME_CHARSET', 'utf-8')
    gzip = setting('AWS_IS_GZIPPED', False)
    preload_metadata = setting('AWS_PRELOAD_METADATA', False)
    gzip_content_types = setting('GZIP_CONTENT_TYPES', (
        'text/css',
        'application/javascript',
        'application/x-javascript',
    ))
    url_protocol = setting('AWS_S3_URL_PROTOCOL', 'http:')
    host = setting('AWS_S3_HOST', S3Connection.DefaultHost)
    use_ssl = setting('AWS_S3_USE_SSL', True)
    port = setting('AWS_S3_PORT', None)

    # The max amount of memory a returned file can take up before being
    # rolled over into a temporary file on disk. Default is 0: Do not roll over.
    max_memory_size = setting('AWS_S3_MAX_MEMORY_SIZE', 0)

    def __init__(self, acl=None, bucket=None, **settings):
        # check if some of the settings we've provided as class attributes
        # need to be overwritten with values passed in here
        for name, value in settings.items():
            if hasattr(self, name):
                setattr(self, name, value)

        # For backward-compatibility of old differing parameter names
        if acl is not None:
            self.default_acl = acl
        if bucket is not None:
            self.bucket_name = bucket

        self.location = (self.location or '').lstrip('/')
        # Backward-compatibility: given the anteriority of the SECURE_URL setting
        # we fall back to https if specified in order to avoid the construction
        # of unsecure urls.
        if self.secure_urls:
            self.url_protocol = 'https:'

        self._entries = {}
        self._bucket = None
        self._connection = None

        if not self.access_key and not self.secret_key:
            self.access_key, self.secret_key = self._get_access_keys()

    @property
    def connection(self):
        if self._connection is None:
            self._connection = self.connection_class(
                self.access_key,
                self.secret_key,
                is_secure=self.use_ssl,
                calling_format=self.calling_format,
                host=self.host,
                port=self.port,
            )
        return self._connection

    @property
    def bucket(self):
        """
        Get the current bucket. If there is no current bucket object
        create it.
        """
        if self._bucket is None:
            self._bucket = self._get_or_create_bucket(self.bucket_name)
        return self._bucket

    @property
    def entries(self):
        """
        Get the locally cached files for the bucket.
        """
        if self.preload_metadata and not self._entries:
            self._entries = dict((self._decode_name(entry.key), entry)
                                for entry in self.bucket.list(prefix=self.location))
        return self._entries

    def _get_access_keys(self):
        """
        Gets the access keys to use when accessing S3. If none
        are provided to the class in the constructor or in the
        settings then get them from the environment variables.
        """
        def lookup_env(names):
            for name in names:
                value = os.environ.get(name)
                if value:
                    return value
        access_key = self.access_key or lookup_env(self.access_key_names)
        secret_key = self.secret_key or lookup_env(self.secret_key_names)
        return access_key, secret_key

    def _get_or_create_bucket(self, name):
        """
        Retrieves a bucket if it exists, otherwise creates it.
        """
        try:
            return self.connection.get_bucket(name,
                validate=self.auto_create_bucket)
        except self.connection_response_error:
            if self.auto_create_bucket:
                bucket = self.connection.create_bucket(name)
                bucket.set_acl(self.bucket_acl)
                return bucket
            raise ImproperlyConfigured("Bucket %s does not exist. Buckets "
                                       "can be automatically created by "
                                       "setting AWS_AUTO_CREATE_BUCKET to "
                                       "``True``." % name)

    def _clean_name(self, name):
        """
        Cleans the name so that Windows style paths work
        """
        # Normalize Windows style paths
        clean_name = posixpath.normpath(name).replace('\\', '/')

        # os.path.normpath() can strip trailing slashes so we implement
        # a workaround here.
        if name.endswith('/') and not clean_name.endswith('/'):
            # Add a trailing slash as it was stripped.
            return clean_name + '/'
        else:
            return clean_name

    def _normalize_name(self, name):
        """
        Normalizes the name so that paths like /path/to/ignored/../something.txt
        work. We check to make sure that the path pointed to is not outside
        the directory specified by the LOCATION setting.
        """
        try:
            return safe_join(self.location, name)
        except ValueError:
            raise SuspiciousOperation("Attempted access to '%s' denied." %
                                      name)

    def _encode_name(self, name):
        return smart_str(name, encoding=self.file_name_charset)

    def _decode_name(self, name):
        return force_unicode(name, encoding=self.file_name_charset)

    def _compress_content(self, content):
        """Gzip a given string content."""
        zbuf = StringIO()
        zfile = GzipFile(mode='wb', compresslevel=6, fileobj=zbuf)
        try:
            zfile.write(content.read())
        finally:
            zfile.close()
        zbuf.seek(0)
        content.file = zbuf
        content.seek(0)
        return content

    def _open(self, name, mode='rb'):
        name = self._normalize_name(self._clean_name(name))
        f = self.file_class(name, mode, self)
        if not f.key:
            raise IOError('File does not exist: %s' % name)
        return f

    def _save(self, name, content):
        cleaned_name = self._clean_name(name)
        name = self._normalize_name(cleaned_name)
        headers = self.headers.copy()
        content_type = getattr(content, 'content_type',
            mimetypes.guess_type(name)[0] or self.key_class.DefaultContentType)

        # setting the content_type in the key object is not enough.
        headers.update({'Content-Type': content_type})

        if self.gzip and content_type in self.gzip_content_types:
            content = self._compress_content(content)
            headers.update({'Content-Encoding': 'gzip'})

        content.name = cleaned_name
        encoded_name = self._encode_name(name)
        key = self.bucket.get_key(encoded_name)
        if not key:
            key = self.bucket.new_key(encoded_name)
        if self.preload_metadata:
            self._entries[encoded_name] = key

        key.set_metadata('Content-Type', content_type)
        self._save_content(key, content, headers=headers)
        return cleaned_name

    def _save_content(self, key, content, headers):
        # only pass backwards incompatible arguments if they vary from the default
        kwargs = {}
        if self.encryption:
            kwargs['encrypt_key'] = self.encryption
        key.set_contents_from_file(content, headers=headers,
                                   policy=self.default_acl,
                                   reduced_redundancy=self.reduced_redundancy,
                                   rewind=True, **kwargs)

    def delete(self, name):
        name = self._normalize_name(self._clean_name(name))
        self.bucket.delete_key(self._encode_name(name))

    def exists(self, name):
        name = self._normalize_name(self._clean_name(name))
        if self.entries:
            return name in self.entries
        k = self.bucket.new_key(self._encode_name(name))
        return k.exists()

    def listdir(self, name):
        name = self._normalize_name(self._clean_name(name))
        # for the bucket.list and logic below name needs to end in /
        # But for the root path "" we leave it as an empty string
        if name and not name.endswith('/'):
            name += '/'

        dirlist = self.bucket.list(self._encode_name(name))
        files = []
        dirs = set()
        base_parts = name.split("/")[:-1]
        for item in dirlist:
            parts = item.name.split("/")
            parts = parts[len(base_parts):]
            if len(parts) == 1:
                # File
                files.append(parts[0])
            elif len(parts) > 1:
                # Directory
                dirs.add(parts[0])
        return list(dirs), files

    def size(self, name):
        name = self._normalize_name(self._clean_name(name))
        if self.entries:
            entry = self.entries.get(name)
            if entry:
                return entry.size
            return 0
        return self.bucket.get_key(self._encode_name(name)).size

    def modified_time(self, name):
        name = self._normalize_name(self._clean_name(name))
        entry = self.entries.get(name)
        # only call self.bucket.get_key() if the key is not found
        # in the preloaded metadata.
        if entry is None:
            entry = self.bucket.get_key(self._encode_name(name))
        # Parse the last_modified string to a local datetime object.
        return parse_ts_extended(entry.last_modified)

    def url(self, name, headers=None, response_headers=None):
        # Preserve the trailing slash after normalizing the path.
        name = self._normalize_name(self._clean_name(name))
        if self.custom_domain:
            return "%s//%s/%s" % (self.url_protocol,
                                  self.custom_domain, filepath_to_uri(name))
        return self.connection.generate_url(self.querystring_expire,
            method='GET', bucket=self.bucket.name, key=self._encode_name(name),
            headers=headers,
            query_auth=self.querystring_auth, force_http=not self.secure_urls,
            response_headers=response_headers)

    def get_available_name(self, name):
        """ Overwrite existing file with the same name. """
        if self.file_overwrite:
            name = self._clean_name(name)
            return name
        return super(S3BotoStorage, self).get_available_name(name)