import logging
from unittest import TestCase

#from local.data.create_dev_db import create_dev_db
from qsic.performers.models import Performer

logger = logging.getLogger(__name__)

TEST_PERFORMER_URI = ('http://newyork.improvteams.com/'
                      'performers/2849/paullogston')

class PerformerModelIntegrationTests(TestCase):

    def test__000_save_it_content_populates_object_as_expected(self):
        p = Performer.objects.create(it_url=TEST_PERFORMER_URI)
        p.save_it_content_from_parsed_it_url()
        self.assertEqual(p.first_name, 'Paul')
        self.assertEqual(p.last_name, 'Logston')
        self.assertEqual(p.it_id, 2849)
        self.assertIsNotNone(p.bio)

    def test__001_save_it_content_returns_false_with_no_it_url_set(self):
        p = Performer.objects.create()
        r = p.save_it_content_from_parsed_it_url()
        self.assertFalse(r['success'])

    def test__002_fetch_headshot_retrieves_and_stores_file(self):
        p = Performer.objects.create(it_url=TEST_PERFORMER_URI)
        p.save_it_content_from_parsed_it_url()
        self.assertTrue(p.fetch_headshot()['success'])

    def test__003_fetch_headshot_returns_false_on_no_it_id(self):
        p = Performer.objects.create()
        self.assertFalse(p.fetch_headshot()['success'])
