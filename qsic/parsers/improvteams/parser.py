import urllib.request

from bs4 import BeautifulSoup
from bs4 import SoupStrainer

class BaseItParser(object):
    """Base Improvteams Parser"""
    def __init__(self, url=None, *args, **kwargs):
        self.url = url
        self.response_status = None
        self.html = None
        self.soup = None
        if self.url:
            self.fetch_html()

    # TODO make getter and setter for html that updates soup

    def fetch_html(self):
        """Fetch and store HTML data from Improvteams.com (ie. self.url)"""
        with urllib.request.urlopen(self.url) as r:
            self.html = r.read()
            self.response_status = r.status

    def parse_soup(self):
        """Parse out divs into bs4 tree/soup"""
        strainer = SoupStrainer(id='main')
        self.soup = BeautifulSoup(self.html, parse_only=strainer)


class ItPerformerParser(BaseItParser):
    """Parser for performer information from Improvteams"""
    def __init__(self, url=None, *args, **kwargs):
        super().__init__(url)
        self.first_name = None
        self.last_name = None
        self.headshot = None
        self.bio = None
        self.parse_html()

    def parse_html(self):
        """Return self with attributes populated"""
        pass

    def fetch_headshot(self):
        """Fetch bytes of headshot"""
        pass

class ItTeamParser(BaseItParser):
    """Parse team information from Improvteams"""
    pass




"""
# store time as big endian long in a string
s = struct.pack("!L", int(time.time()))
rand_hash = base64.urlsafe_b64encode(s)[:-2]
new_headshot_filename = '%s-%s-%s' % (rand_hash, self.first_name, self.last_name)

if self.headshot:
    self.headshot.delete(save=False)

if player_info.headshot:
    self.headshot.save('%s.jpg' % slugify(new_headshot_filename),
                       File(open(player_info.headshot)))
    os.unlink(player_info.headshot)
"""





"""
import sys
import contextlib
import urllib, urllib2
from bs4 import BeautifulSoup, SoupStrainer
from django.conf import settings
from django.utils import encoding
from stringutils import convert_smart_quotes

import requests
import boto
from boto.s3.key import Key

#c = boto.connect_s3()
#b = c.get_bucket('qsic-staging')

class ImprovteamsPlayerInfo(object):
    def __init__(self, url = None, *args, **kwargs):
        self.url = url
        self.headshot = None
        self.bio = None
        self.first_name = None
        self.last_name = None
        self.get_info()
        return self

    def get_info(self):
        with contextlib.closing(urllib.urlopen(self.url)) as usock:
            html = encoding.smart_unicode(usock.read())

        tree = BeautifulSoup(html, parse_only=SoupStrainer('div'))
        name = tree.find('div', class_="profile_right").h1.em.get_text().split(' ')
        headshot = tree.find('div', class_="photo").img
        bio = tree.find('div', class_="bio")

        self.bio = ''.join([convert_smart_quotes(c.encode("utf-8"))
                            for c in bio.contents]).strip()
        self.first_name = name[0].encode("utf-8", "ignore").title()
        self.last_name = name[1].encode("utf-8", "ignore").title()

        if headshot and headshot.attrs['src']:
            self.headshot = ('players/temp-%s-%s.jpg' %
                             (self.first_name, self.last_name))
            it_headshot_url = ('http://newyork.improvteams.com%s' %
                               headshot.attrs['src'])
            data = requests.get(it_headshot_url)
            #k = Key(b)
            #k.key = 'media/' + self.headshot
            #k.set_contents_from_string(data.content)

        return self

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    def __unicode__(self):
        return '%s %s (%s)' % (self.first_name, self.last_name, self.url)


class ImprovteamsTeamInfo(object):
    def __init__(self, url = None, *args, **kwargs):
        self.url = url
        self.team_name = None
        self.players = None
        self.profile = None
        self.team_photo = None

    @property
    def url(self):
        return self.url

    @url.setter
    def url(self, url):
        self.url = url[:-1] if url[-1] == '/' else url

    def get_info(self):
        with contextlib.closing(urllib.urlopen(self.url)) as usock:
            html = usock.read().decode('cp1252')

        tree = BeautifulSoup(html, parse_only=SoupStrainer('div'))
        new_profile = tree.find('div', id="plus_image_wrapper")

        if not new_profile:
            return self.parse_old_profile(tree)

        team_name = new_profile.find('div', class_="team_name_1")
        if team_name:
            self.team_name = team_name.get_text()
        else:
            self.team_name = 'not-available'
        self.players = self.process_players(tree)

        bio = tree.find('div', class_="bio").extract()
        for nested_div in [t.extract() for t in bio.find_all('div')]:
            nested_div.decompose()

        self.profile = bio.get_text().strip()

        self.get_team_photo(new_profile.find('img', alt="team_image"))

        return self

    def parse_old_profile(self, tree):
        old_profile = tree.find('div', class_="profile_right")

        ret_val = {}
        self.team_name = old_profile.h1.em.get_text().strip()
        team_photo = tree.find('div', class_="photo_and_links")
        clear_div = old_profile.find('div', class_="clear")
        bio_nodes = [s.strip() for s in clear_div.find_next_siblings(text=True) if s != None and len(s.strip()) > 0]
        self.profile = bio_nodes[0]
        self.players = self.process_players(tree)
        self.get_team_photo(team_photo.find('div', class_="photo").img)
        return self

    def get_team_photo(self, img_src):
        if img_src and img_src.attrs['src']:
            self.team_photo = 'uploads/teams/temp-%s.jpg' % (self.team_name)
            urllib.urlretrieve('http://newyork.improvteams.com%s' % img_src.attrs['src'], self.team_photo)

    def process_players(self, tree):
        people = tree.find('div', class_="people thumbnails").find_all('a', class_="thumb")

        players = []
        for a in people:
            player_info = ImprovteamsPlayerInfo(a.attrs['href'])
            players.append(player_info)

        return players
"""