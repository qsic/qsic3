import base64
import struct
import os
import re
import time
import urllib.parse

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.core.files import File

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

    def parse_it_id_from_url(self):
        """Parse Improvteam ID from performer URL
        ex. http://newyork.improvteams.com/performers/2849/paullogston
        ex. sets self.it_id = 2849
        """
        path = urllib.parse.urlparse(self.it_url)[2]
        match = re.match(r""".*/(\d+)/.*""", path)
        if match:
            self.it_id = int(match.group(1))

    def save_it_content_from_parsed_url(self, url=None):
        """Save Player info parsed from Improvteams.com
            Return True on successful completion
        """
        if url is not None:
            self.it_url = url
            self.parse_it_id_from_url()

        # Return False if URL passed doesn not save to model
        # eg. invalid URL
        if not self.it_url:
            return False

        # Parse player info from URL
        player_info = ParsePlayerInfo(self.it_url)

        self.first_name = player_info.first_name
        self.last_name = player_info.last_name
        self.bio = ('%s'
                    '<br>'
                    'Bio courtesy of <a href="%s">%s</a>' %
                    (player_info.bio, player_info.url, player_info.url))
        self.headshot = player_info.headshot
        self.save()
        return True