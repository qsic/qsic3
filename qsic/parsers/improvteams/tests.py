import os.path
import sys
import unittest
import urllib

from django.core.files import File

from project_settings.settings import PROJECT_ROOT
from qsic.parsers.improvteams.parser import BaseItParser
from qsic.parsers.improvteams.parser import ItPerformerParser
from qsic.parsers.improvteams.parser import ItTeamParser

"""The file at this location holds the HTML that will be tested
against to see if the format of performer pages has changed.
"""
CONTROL_PERFORMER_URI = os.path.join(PROJECT_ROOT,
                                      'local',
                                      'test_data',
                                      'it_performer_page_paullogston.html')

"""The file at this URI will be tested against the control perfomer page to
see if any changes in the format of the HTML.
"""
TEST_PERFORMER_URI = ('http://newyork.improvteams.com/'
                       'performers/2849/paullogston')

"""The file at this location holds the HTML that will be tested
against to see if the format of teams pages has changed.
"""
CONTROL_TEAM_URI = os.path.join(PROJECT_ROOT,
                                'local',
                                'test_data',
                                'it_team_page_bearcountry.html')

"""The file at this URI will be tested against the control team page to
see if any changes in the format of the HTML.
"""
TEST_TEAM_URI = 'http://bearcountry.improvteams.com/'

def get_control_html_from_lfs(path):
    with open(path) as fp:
        return fp.read()


class BaseItParserUTs(unittest.TestCase):
    """Common Unit Tests to all Parser test objects"""
    pass

class ParserUTsMixin(object):
    """Unit tests common to all parser objects"""
    def test__fetch_html_returns_200(self):
        """Fetch returns status code of 200"""
        parser = BaseItParser(self.__class__.test_uri)
        self.assertEqual(parser.response_status, 200)


class ItPerformerParserUTs(unittest.TestCase, ParserUTsMixin):
    """Performer Parser Unit Tests"""
    @classmethod
    def setUpClass(cls):
        cls.test_uri = TEST_PERFORMER_URI
        cls.control_uri = CONTROL_PERFORMER_URI

        cls.test_parser = ItPerformerParser(cls.test_uri)
        cls.control_parser = ItPerformerParser(None)
        cls.control_parser.html = get_control_html_from_lfs(cls.control_uri)

    def test__it_id_parsed_from_it_url(self):
        self.assertEqual(self.__class__.test_parser.it_id, 2849)

    def test__bio_parsed_as_expected(self):
        """Checks for changes in the structure of bio at Improvteams.com"""
        control_bio = self.__class__.control_parser.soup.select('#main '
                                                     '.profile '
                                                     '.profile_right '
                                                     '.bio')[0].string
        test_bio = self.__class__.test_parser.soup.select('#main '
                                               '.profile '
                                               '.profile_right '
                                               '.bio')[0].string
        self.assertEqual(test_bio, control_bio)

    def test__name_parsed_as_expected(self):
        """Check for changes in structure of name"""
        self.assertEqual(self.__class__.test_parser.first_name,
                         self.__class__.control_parser.first_name)
        self.assertEqual(self.__class__.test_parser.last_name,
                         self.__class__.control_parser.last_name)
        self.assertEqual(self.__class__.test_parser.first_name,
                         'Paul')
        self.assertEqual(self.__class__.test_parser.last_name,
                         'Logston')


class ItTeamParserUTs(unittest.TestCase, ParserUTsMixin):
    """Team Parser Unit Tests"""
    @classmethod
    def setUpClass(cls):
        cls.control_uri = CONTROL_TEAM_URI
        cls.test_uri = TEST_TEAM_URI

        cls.test_parser = ItTeamParser(cls.test_uri)
        cls.control_parser = ItTeamParser(None)
        cls.control_parser.html = get_control_html_from_lfs(cls.control_uri)

    def test__team_name_parsed_as_expected(self):
        """Check for changes in structure of HTML effecting team name"""
        self.assertEqual(self.__class__.test_parser.team_name,
                         self.__class__.control_parser.team_name)
        self.assertEqual(self.__class__.test_parser.team_name, 'Bear Country')

    def test__team_photo_uri_parsed_as_expected(self):
        """Check for changes in structure of HTML effecting team photo uri"""
        self.assertEqual(self.__class__.test_parser.team_photo_uri,
                         self.__class__.control_parser.team_photo_uri)

    def test__team_bio_parsed_as_expected(self):
        """Check for changes in structure of HTML effecting team bio"""
        self.assertEqual(self.__class__.test_parser.team_bio,
                         self.__class__.control_parser.team_bio)

    def test__performer_uri_list_parsed_as_expected(self):
        """Check for changes in structure of HTML effecting performer list"""
        self.assertEqual(self.__class__.test_parser.performer_uri_list,
                         self.__class__.control_parser.performer_uri_list)
        self.assertEqual(self.__class__.test_parser.performer_uri_list,
            ['http://newyork.improvteams.com/performers/2872/mike_lane',
             'http://newyork.improvteams.com/performers/2849/paul_logston'])