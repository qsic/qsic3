import logging
import os.path
import sys
import unittest
import urllib

from django.core.files import File

from project_settings.settings.base import PROJECT_ROOT
from qsic.parsers.improvteams.parser import BaseItParser
from qsic.parsers.improvteams.parser import ItPerformerParser
from qsic.parsers.improvteams.parser import ItTeamParser

logger = logging.getLogger(__name__)

"""The file at this location holds the HTML that will be tested
against to see if the format of teams pages has changed.
"""
CONTROL_TEAM_URI_PLAIN = local_data_path('it_team_page_amanda_and_jenice.html')

"""The file at this URI will be tested against the control team page to
see if any changes in the format of the HTML.
"""
#TEST_TEAM_URI_PLAIN = 'http://bearcountry.improvteams.com/'
TEST_TEAM_URI_PLAIN = 'http://amandajenice.improvteams.com/'

"""Similar to above however this will be tested against a different
Improvteams.com Team page format. The format here has a main photo
that consumes most of the page.
"""
CONTROL_TEAM_URI_PLUS = local_data_path('it_team_page_boat.html')

TEST_TEAM_URI_PLUS = 'http://boat.improvteams.com/'


test_relations = {
    'Paul': {
        'control': 'it_performer_page_paullogston.html',
        'test': 'http://newyork.improvteams.com/performers/2849/paullogston'
    },
}


def local_data_path(file_name):
    """
    Return absolute path of file file_name
    located in local/test_data
    """
    return os.path.join(PROJECT_ROOT, 'local', 'test_data', file_name)


def get_control_html_from_lfs(path):
    with open(path) as fp:
        return fp.read()


class BaseItParserUTs(unittest.TestCase):
    """Common Unit Tests to all Parser test objects"""
    pass


class ParserUTsMixin(object):
    """Unit tests common to all parser objects"""
    def test__000_fetch_html_returns_200(self):
        """Fetch returns status code of 200"""
        parser = BaseItParser(self.__class__.test_uri)
        self.assertEqual(parser.response_status, 200)


class ItPerformerParserUTs(unittest.TestCase, ParserUTsMixin):
    """Performer Parser Unit Tests"""
    test_relation = test_relations['Paul']
    test_uri = test_relation['test']
    control_uri = test_relation['control']

    @classmethod
    def setUpClass(cls):
        cls.test_parser = ItPerformerParser(cls.test_uri)
        cls.control_parser = ItPerformerParser(None)
        cls.control_parser.html = get_control_html_from_lfs(cls.control_uri)
        cls.control_parser.parse_soup()

    def test__000_it_id_parsed_from_it_url(self):
        self.assertEqual(self.test_parser.it_id, 2849)

    def test__001_bio_parsed_as_expected(self):
        """Checks for changes in the structure of bio at Improvteams.com"""
        selector = '#main .profile .profile_right .bio'
        control_bio = self.control_parser.soup.select(selector)[0].string
        test_bio = self.test_parser.soup.select(selector)[0].string
        self.assertEqual(test_bio, control_bio)

    def test__002_name_parsed_as_expected(self):
        """Check for changes in structure of name"""
        self.assertEqual(self.test_parser.first_name,
                         self.control_parser.first_name)
        self.assertEqual(self.test_parser.last_name,
                         self.control_parser.last_name)
        self.assertEqual(self.test_parser.first_name, 'Paul')
        self.assertEqual(self.test_parser.last_name, 'Logston')


class ItTeamPlainParserUTs(unittest.TestCase, ParserUTsMixin):
    """Team Plain Parser Unit Tests"""
    control_uri = CONTROL_TEAM_URI_PLAIN
    test_uri = TEST_TEAM_URI_PLAIN
    team_name = 'Amanda & Jenic'

    @classmethod
    def setUpClass(cls):
        cls.test_parser = ItTeamParser(cls.test_uri)
        cls.control_parser = ItTeamParser(None)
        cls.control_parser.html = get_control_html_from_lfs(cls.control_uri)
        cls.control_parser.parse_soup()

    def test__000_team_name_parsed_as_expected(self):
        """Check for changes in structure of HTML effecting team name"""
        self.assertEqual(self.test_parser.team_name,
                         self.control_parser.team_name)
        self.assertEqual(self.test_parser.team_name,
                         self.team_name)

    def test__001_team_photo_uri_parsed_as_expected(self):
        """Check for changes in structure of HTML effecting team photo uri"""
        self.assertEqual(self.test_parser.team_photo_uri,
                         self.control_parser.team_photo_uri)

    def test__002_team_bio_parsed_as_expected(self):
        """Check for changes in structure of HTML effecting team bio"""
        self.assertEqual(self.test_parser.team_bio,
                         self.control_parser.team_bio)

    def test__003_performer_uri_list_parsed_as_expected(self):
        """Check for changes in structure of HTML effecting performer list"""
        self.assertEqual(self.test_parser.performer_uri_list,
                         self.control_parser.performer_uri_list)


class ItTeamPlusParserUTs(ItTeamPlainParserUTs):
    """Team Plus Parser Unit Tests"""
    control_uri = CONTROL_TEAM_URI_PLUS
    test_uri = TEST_TEAM_URI_PLUS
    team_name = 'Boat'