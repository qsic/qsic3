import os.path
import unittest

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
    pass

class ParserUTsMixin(object):
    def test__fetch_html_returns_200(self):
        """Fetch returns status code of 200"""
        parser = BaseItParser(self.test_uri)
        self.assertEqual(parser.response_status, 200)


class ItPerformerParserUTs(unittest.TestCase, ParserUTsMixin):

    def setUp(self):
        self.control_uri = CONTROL_PERFORMER_URI
        self.test_uri = TEST_PERFORMER_URI


    def test__soup_generated_as_expected(self):
        """Checks for changes in the structure of Improvteams.com"""
        control_parser = BaseItParser(None)
        control_parser.html = get_control_html_from_lfs(self.control_uri)
        control_parser.parse_soup() # cut this out after getter/setter made
        control_bio = control_parser.soup.select('#main '
                                                 '.profile '
                                                 '.profile_right '
                                                 '.bio')[0].string

        test_parser = BaseItParser(self.test_uri)
        test_parser.parse_soup() # cut this out after getter/setter made
        test_bio = test_parser.soup.select('#main '
                                           '.profile '
                                           '.profile_right '
                                           '.bio')[0].string

        self.assertEqual(control_bio, test_bio)


class ItTeamParserUTs(unittest.TestCase, ParserUTsMixin):
    def setUp(self):
        self.control_uri = CONTROL_TEAM_URI
        self.test_uri = TEST_PERFORMER_URI