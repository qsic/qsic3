import re
import socket
import urllib

from bs4 import BeautifulSoup
from bs4 import SoupStrainer


class BaseItParser(object):
    """Base Improvteams Parser"""
    def __init__(self, url=None, *args, **kwargs):
        self.url = url
        self.response_status = None
        self._html = None
        self.soup = None
        if self.url:
            self.fetch_html()

    @property
    def html(self):
        return self._html

    @html.setter
    def html(self, value):
        self._html = value
        self.load_soup()

    def fetch_html(self):
        """Fetch and store HTML data from Improvteams.com (ie. self.url)"""
        try:
            with urllib.request.urlopen(self.url) as r:
                self.response_status = r.status
                if r.status == 200:
                    self.html = r.read()
        except socket.gaierror:
            self.response_status = -1

    def load_soup(self):
        """Load main div into bs4 tree/soup"""
        strainer = SoupStrainer(id='main')
        self.soup = BeautifulSoup(self.html, parse_only=strainer)

    def __str__(self):
        return self.url


class ItPerformerParser(BaseItParser):
    """Parser for performer information from Improvteams"""
    def __init__(self, url=None, *args, **kwargs):
        self.it_id = None
        self.first_name = None
        self.last_name = None
        self.headshot_uri = None
        self.bio = None
        super().__init__(url)

    def load_soup(self):
        """Override and add a few more parsings of the soup"""
        super().load_soup()
        self.parse_it_id_from_url()
        self.parse_soup_for_bio()
        self.parse_soup_for_name()

    def parse_it_id_from_url(self):
        """Parse Improvteam ID from performer URL
        ex. http://newyork.improvteams.com/performers/2849/paullogston
        ex. sets self.it_id = 2849
        """
        path = urllib.parse.urlparse(self.url)[2]
        match = re.match(""".*/(\d+)/.*""", str(path))
        if match:
            self.it_id = int(match.group(1))

    def parse_soup_for_name(self):
        """Return self with first and last name populated"""
        raw_name = self.soup.select('#main .profile .profile_right '
                                    'h1 em')[0].string.strip()
        name_list = raw_name.split(' ')
        self.first_name = name_list[0]
        self.last_name = " ".join(name_list[1:])

    def parse_soup_for_bio(self):
        """Return self with bio populated"""
        bio = self.soup.select('#main .profile .profile_right .bio')[0].text
        if self.bio:
            self.bio = bio.strip()


class ItTeamParser(BaseItParser):
    """Parse team information from Improvteams"""
    def __init__(self, url=None, *args, **kwargs):
        self.team_name = None
        self.team_photo_uri = None
        self.team_bio = None
        self.performer_uri_list = None
        super().__init__(url)

    def load_soup(self):
        """Override and add a few more parsings of the soup"""
        super().load_soup()
        self.parse_soup_for_team_name()
        self.parse_soup_for_team_photo_uri()
        self.parse_soup_for_team_bio()
        self.parse_soup_for_performer_uri_list()

    def parse_soup_for_team_name(self):
        """Return self with team_name populated"""
        selector = '#main .profile .profile_right h1 em'
        name = self.soup.select(selector)[0].string
        if name:
            self.team_name = name.strip()

    def parse_soup_for_team_photo_uri(self):
        """Return self with team photo uri populated"""
        selector = '#main .profile .profile_right h1 em'
        uri = self.soup.select(selector)[0]
        if uri:
            pass

    def parse_soup_for_team_bio(self):
        """Return self with team bio populated"""
        profile_right = self.soup.select('#main .profile .profile_right')[0]
        try:
            iframe = str(profile_right).split('</iframe>')[1]
            team_bio = iframe.split('<div class="clear"></div>')[1]
            team_bio = team_bio.replace('<br/>', '').strip()
        except ValueError:
            return
        if team_bio:
            self.team_bio = team_bio

    def parse_soup_for_performer_uri_list(self):
        """Return self with performer uri list populated"""
        selector = '#main .profile .profile_right .people.thumbnails'
        performer_div_list = self.soup.select(selector)[0]
        performer_uri_list = []
        for a in performer_div_list.find_all('a'):
            performer_uri_list.append(a['href'])
        self.performer_uri_list = performer_uri_list
