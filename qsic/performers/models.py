import urllib.request

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db import models

from qsic.parsers.improvteams.parser import ItPerformerParser


class Performer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    # 'it' is short for Imrpovteams / Improvteams.com
    it_url = models.URLField(null=True, blank=True)
    it_id = models.PositiveIntegerField(null=True, blank=True)
    headshot = models.ImageField(upload_to='performers/headshots',
                                 null=True,
                                 blank=True)
    bio = models.TextField(null=True, blank=True)

    class Meta:
        app_label = 'qsic'

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

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

        self.bio = ('%s'
                    '<br>'
                    'Bio courtesy of <a href="%s">Improvteams.com</a>' %
                    (performer_info.bio, performer_info.url))

        self.save()
        return {'success': True}

    def fetch_headshot(self):
        """Fetch and save headshot photo from Improvteams.com"""
        if not self.it_id:
            return False
        uri = ''.join(['http://newyork.improvteams.com/',
                       'uploads/performer_images/performer_',
                       str(self.it_id),
                       '.jpg'])
        with urllib.request.urlopen(uri) as imgp:
            # make sure imgp is a jpeg
            if imgp.info().get_content_type() == 'image/jpeg':
                name = str(self.it_id) + '.jpg'
                self.headshot.save(name, ContentFile(imgp.read()), save=True)
                return True
            else:
                return False    # maybe leave this out so we return none
