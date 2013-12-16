import logging
import re
import socket
import urllib

from bs4 import BeautifulSoup
from bs4 import SoupStrainer

logger = logging.getLogger(__name__)


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
        self.soup = BeautifulSoup(self.html, 'html.parser')

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
        if self.soup:
            self.parse_soup()

    def parse_soup(self):
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
        self.parser_plus = False
        self.team_name = None
        self.team_photo_uri = None
        self.team_bio = None
        self.performer_uri_list = None
        super().__init__(url)
        if self.soup:
            self.parse_soup()

    def parse_soup(self):
        # check to see if page uses <div id="plus_image_wrapper"...>
        selector_plus = '#main #plus_image_wrapper'
        if self.soup.select(selector_plus):
            self.parser_plus = True
        self.parse_html_head_for_team_name()
        self.parse_soup_for_team_photo_uri()
        self.parse_soup_for_team_bio()
        self.parse_soup_for_performer_uri_list()

    def parse_html_head_for_team_name(self):
        """Return self with team_name populated"""
        selector = 'html head title'
        title_leaf = BeautifulSoup(self.html).select(selector)
        if title_leaf:
            title = title_leaf[0].string
            if title:
                self.team_name = title.strip('| New York Improv Teams')

    def parse_soup_for_team_photo_uri(self):
        """Return self with team photo uri populated"""
        selector = '#main .profile .photo_and_links .photo img'
        if self.parser_plus:
            selector = '#main #plus_image_wrapper img'
        uri_leaf = self.soup.select(selector)
        if uri_leaf:
            uri = uri_leaf[0]
            if uri and hasattr(uri, 'src'):
                self.team_photo_uri = uri['src']

    def parse_soup_for_team_bio(self):
        """Return self with team bio populated"""
        team_bio = None
        if self.parser_plus:
            selector = '#main .profile .bio'
            bio_leaf = self.soup.select(selector)
            if bio_leaf:
                bio_list = bio_leaf[0].get_text().split('\n\n')
                team_bio = bio_list[2]
                team_bio = team_bio.strip() if team_bio else team_bio
        else:
            selector = '#main .profile .profile_right'
            profile_right = self.soup.select(selector)
            iframe = str(profile_right).split('</iframe>')[1]
            team_bio = iframe.split('<div class="clear"></div>')[1]
            team_bio = team_bio.replace('<br/>', '').strip()

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
