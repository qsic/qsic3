import logging
import os
import urllib.request

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify

from image_cropping.fields import ImageRatioField

from py3s3.files import S3ContentFile
from parsers.improvteams.parser import ItPerformerParser

logger = logging.getLogger(__name__)


class Performer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    slug = models.SlugField(blank=True, default='')
    # 'it' is short for Imrpovteams / Improvteams.com
    it_url = models.URLField(null=True, blank=True)
    it_id = models.PositiveIntegerField(null=True, blank=True, unique=True)
    photo = models.ImageField(upload_to='performers/photos', null=True, blank=True)
    detail_crop = ImageRatioField('photo', '300x300', size_warning=True)
    bio = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name

    def type(self):
        return self.__class__.__name__

    def save(self, **kwargs):
        self.slug = slugify(' '.join((self.first_name, self.last_name)))
        super().save()

    @property
    def url(self):
        url = reverse('performers:performer_detail_view_add_slug', kwargs={'pk': self.id})
        url = ''.join((url, '/', self.slug))
        return url

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def save_it_content_from_parsed_it_url(self):
        """Save Performer info parsed from Improvteams.com
            Return True on successful completion
        """

        # Return False if URL passed does not save to model
        # eg. invalid URL
        if not self.it_url:
            return {'success': False, 'msg': 'It url is not set.'}

        # Parse performer info from URL
        try:
            performer_info = ItPerformerParser(self.it_url)
        except:
            return {'success': False, 'msg': 'Unable to parse performer info.'}

        self.it_id = performer_info.it_id
        self.first_name = performer_info.first_name
        self.last_name = performer_info.last_name

        # print(performer_info.bio)
        self.bio = performer_info.bio

        self.save()
        return {'success': True}

    def fetch_headshot(self):
        """Fetch and save headshot photo from Improvteams.com"""
        if not self.it_id:
            return {'success': False, 'msg': 'Improvteams id is not set.'}
        uri = ''.join(['http://newyork.improvteams.com/uploads/performer_images/performer_',
                       str(self.it_id),
                       '.jpg'])
        with urllib.request.urlopen(uri) as imgp:
            # make sure resource has a content-length
            if not 'Content-Length' in imgp.headers:
                return None
            content_length = int(imgp.headers['Content-Length'])
            content = imgp.read(content_length)
            # make sure imgp is a jpeg
            mimetype = 'image/jpeg'
            if imgp.info().get_content_type() == mimetype:
                file_name = str(self.it_id) + '.jpg'
                s3file = S3ContentFile(content, name=file_name, mimetype=mimetype)
                self.photo.save(file_name, s3file, save=True)
                return {'success': True}
        return {'success': False, 'msg': 'Unable to save headshot.'}

    def load_from_it(self):
        self.save_it_content_from_parsed_it_url()
        self.fetch_headshot()
        # save default dims of photo
        if self.photo:
            self.detail_crop = ','.join(('0', '0', str(self.photo.width), str(self.photo.height)))
            self.save()
        return True

    def groups(self):
        """
        Return iterable of groups that the user is in.
        """
        return [gpr.group for gpr in self.groupperformerrelation_set.order_by('-start_dt')]

