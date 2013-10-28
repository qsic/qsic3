import json
import os.path

from local_dev.settings import SITE_ROOT

DEV_DATA_ROOT = os.path.join(SITE_ROOT, 'local_dev', 'data')

with open(os.path.join(DEV_DATA_ROOT, 'dev_players.json'), 'rt') as fp:
    dev_players = json.load(fp)

with open(os.path.join(DEV_DATA_ROOT, 'dev_teams.json'), 'rt') as fp:
    dev_teams = json.load(fp)

with open(os.path.join(DEV_DATA_ROOT, 'dev_teamphotos.json'), 'rt') as fp:
    dev_teamphotos = json.load(fp)

with open(os.path.join(DEV_DATA_ROOT, 'dev_playerteams.json'), 'rt') as fp:
    dev_playerteams = json.load(fp)

with open(os.path.join(DEV_DATA_ROOT, 'dev_shows.json'), 'rt') as fp:
    dev_shows = json.load(fp)

with open(os.path.join(DEV_DATA_ROOT, 'dev_showphotos.json'), 'rt') as fp:
    dev_showphotos = json.load(fp)

with open(os.path.join(DEV_DATA_ROOT, 'dev_teamcalendars.json'), 'rt') as fp:
    dev_teamcalendars = json.load(fp)

dev_data = {
    'dev_players': dev_players,
    'dev_teams': dev_teams,
    'dev_teamphotos': dev_teamphotos,
    'dev_playerteams': dev_playerteams,
    'dev_shows': dev_shows,
    'dev_showphotos': dev_showphotos,
    'dev_teamcalendars': dev_teamcalendars,
}