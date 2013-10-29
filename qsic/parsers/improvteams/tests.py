import os.path
import unittest

from project_settings.settings import PROJECT_ROOT
from qsic.parsers.improvteams.parser import BaseItParser
from qsic.parsers.improvteams.parser import ItPerformerParser
from qsic.parsers.improvteams.parser import ItTeamParser


class ItParseUTsMixin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.control_url = ('http://newyork.improvteams.com/'
                           'performers/2849/paullogston')
        cls.control_html = cls.helper__get_control_html_from_lfs()
        cls.test_parser = BaseItParser(cls.control_url)

    @classmethod
    def helper__get_control_html_from_lfs(self):
        with open(
                os.path.join(
                        PROJECT_ROOT,
                        'local',
                        'test_data',
                        'it_performer_page_paullogston.html'
                )) as fp:
            return fp.read()

class BaseItParserUTs(ItParseUTsMixin, unittest.TestCase):
    def test__fetch_html_returns_200(self):
        """Fetch returns status code of 200"""
        parser = self.__class__.test_parser
        self.assertEqual(parser.response_status, 200)

    @unittest.skip('This test is too brittle to run effectively.')
    def test__fetch_html_fetches_correct_html(self):
        """Fetches expected HTML and not a page formatted differently
        or the like
        """
        #parser = BaseItParser(self.url)
        self.assertEqual(True, True)


class ItPerformerParserUTs(ItParseUTsMixin, unittest.TestCase):

    def test__soup_generated_as_expected(self):
        """Checks for changes in the structure of Improvteams.com"""
        control_parser = BaseItParser(None)
        control_parser.html = self.__class__.control_html
        control_parser.parse_soup() # cut this out after getter/setter made
        control_bio = control_parser.soup.select('#main '
                                                 '.profile '
                                                 '.profile_right '
                                                 '.bio')[0].string

        test_parser = self.__class__.test_parser
        test_parser.parse_soup() # cut this out after getter/setter made
        test_bio = test_parser.soup.select('#main '
                                           '.profile '
                                           '.profile_right '
                                           '.bio')[0].string

        self.assertEqual(control_bio, test_bio)


class ItTeamParserUTs(unittest.TestCase):
    pass