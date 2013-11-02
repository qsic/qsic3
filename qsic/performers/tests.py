from django.test import TestCase
from selenium import webdriver

#from local.data.create_dev_db import create_dev_db
from qsic.performers.models import Performer

#TODO port to python3
"""
class PlayerFTs(TestCase):

	@classmethod
	def setUpClass(cls):
		create_dev_db(log=False)

	def setUp(self):
		self.browser = webdriver.Chrome()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_player_appears_in_current_players(self):
		self.browser.get('http://queens-secret.dev/players/')
		players = self.browser.find_elements_by_class_name('player-list')
		player_list = [player.text for player in players]
		self.assertIn(u'Mike Lane', player_list)
		self.assertNotIn(u'Tessa Greenberg', player_list)

	def test_player_appears_in_past_players(self):
		self.browser.get('http://queens-secret.dev/players/past/')
		players = self.browser.find_elements_by_class_name('player-list')
		player_list = [player.text for player in players]
		self.assertIn(u'Tessa Greenberg', player_list)
		#self.assertNotIn(u'Megan Maes', player_list)
"""

class PerformerUTs(TestCase):
    pass