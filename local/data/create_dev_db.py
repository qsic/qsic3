# coding=utf-8
import logging
import sys

from players.models import Player
from shows.models import Show
from shows.models import ShowPhoto
from shows.models import TeamCalendar
from teams.models import Team
from teams.models import TeamPhoto
from teams.models import PlayerTeam

from local_dev.data.dev_data_linker import dev_data

logger = logging.getLogger(__name__)

def create_dev_db(log=False):

    if log:
        logger.setLevel(logging.DEBUG)
        sh = logging.StreamHandler(sys.stdout)
        frmt = logging.Formatter(fmt='%(levelname)s: %(message)s')
        sh.setFormatter(frmt)
        logger.addHandler(sh)

    logger.info('==> Deleting old dev data')

    models = (Player,
              Team,
              TeamPhoto,
              PlayerTeam,
              Show,
              ShowPhoto,
              TeamCalendar)

    [delete_model_objects(model) for model in models]

    logger.info('==> Loading new dev data')

    # players
    players = [create_player(first_name=player['first_name'],
                             last_name=player['last_name'],
                             improvteams_url=player['improvteams_url'],
                             headshot=player['headshot'],
                             bio=player['bio']) for player in dev_data['dev_players']]
    logger.info('%i players created' % len(players))

    # teams
    teams = [create_team(name=team['name'],
                         is_house_team=team['is_house_team'],
                         name_color=team['name_color'],
                         name_shadow_color=team['name_shadow_color'],
                         background_color=team['background_color'],
                         retired=team['retired'],
                         improvteams_url=team['improvteams_url'],
                         website=team['website'],
                         profile=team['profile'],
                         team_logo=team['team_logo'],
                         team_photo=team['team_photo']) for team in dev_data['dev_teams']]
    logger.info('%i teams created' % len(teams))

    # teamphotos
    teamphotos = []
    for teamphoto in dev_data['dev_teamphotos']:
        team = get_team_or_none(teamphoto['team'])
        if team and teamphoto['photo']:
            teamphotos.append(create_teamphoto(team, teamphoto['photo']))
    logger.info('%i teamphotos created' % len(teamphotos))

    # playerteams
    playerteams = []
    for playerteam in dev_data['dev_playerteams']:
        player = get_player_or_none(playerteam['player'])
        team = get_team_or_none(playerteam['team'])
        if player and team:
            playerteams.append(create_playerteam(player, team, playerteam['active']))
    logger.info('%i playerteams created' % len(playerteams))

    # shows
    shows = [create_show(title=show['title'],
                         blurb=show['blurb'],
                         start_date=show['start_date'],
                         active=show['active']) for show in dev_data['dev_shows']]
    logger.info('%i shows created' % len(shows))

    # showphotos
    showphotos = []
    for showphoto in dev_data['dev_showphotos']:
        team = get_team_or_none(showphoto['team'])
        show = get_show_or_none(showphoto['show'], 
                                showphoto['start_date'])
        if team and show:
            showphotos.append(create_showphoto(team, show, showphoto['photo']))
    logger.info('%i showphotos created' % len(showphotos))

    # teamcalendars
    teamcalendars = []
    for teamcalendar in dev_data['dev_teamcalendars']:
        team = get_team_or_none(teamcalendar['team'])
        show = get_show_or_none(teamcalendar['show'], 
                                teamcalendar['start_date'])
        if team and show:
            teamcalendars.append(create_teamcalendar(show,
                                                     team,
                                                     teamcalendar['start_time'],
                                                     teamcalendar['end_time']))
    logger.info('%i teamcalendars created' % len(teamcalendars))

def delete_model_objects(model):
    model_queryset = model.objects.all()
    count = model_queryset.count()
    model_queryset.delete()
    logger.info('Deleted %i %s objects' % (count, model))

def create_player(first_name, last_name, 
                  improvteams_url=None, headshot=None, bio=None, user=None):
    logger.info('Creating player: %s %s' % (first_name, last_name))
    return Player.objects.create(user=user,
                                 first_name=first_name,
                                 last_name=last_name,
                                 improvteams_url=improvteams_url,
                                 headshot=headshot,
                                 bio=bio)

def create_team(name,
                is_house_team=True,
                name_color='#000000',
                name_shadow_color='#ffffff',
                background_color='#ffffff',
                retired=None,
                improvteams_url=None,
                website=None,
                profile=None,
                team_logo=None,
                team_photo=None):
    logger.info('Creating team: %s' % (name))
    return  Team.objects.create(name=name,
                                is_house_team=is_house_team,
                                name_color=name_color,
                                name_shadow_color=name_shadow_color,
                                background_color=background_color,
                                retired=retired,
                                improvteams_url=improvteams_url,
                                website=website,
                                profile=profile,
                                team_logo=team_logo,
                                team_photo=team_photo)

def create_teamphoto(team, photo):
    logger.info('Adding photo %s to team %s' % (photo, team))
    return TeamPhoto.objects.create(team, photo)

def get_player_or_none(player_url):
    p = Player.objects.filter(improvteams_url=player_url)
    if p and len(p) > 1:
        raise ValueError('Two or more Players found with the same improvteams_url')
    try:
        return p[0]
    except IndexError:
        return None

def get_team_or_none(team_name):
    t = Team.objects.filter(name=team_name)
    if t and len(t) > 1:
        raise ValueError('Two or more Teams found with the same name')
    try:
        return t[0]
    except IndexError:
        return None

def get_show_or_none(title, start_date):
    s = Show.objects.filter(title=title).filter(start_date=start_date)
    if s and len(s) > 1:
        raise ValueError('Two or more Shows found with the same title and start_date')
    try:
        return s[0]
    except IndexError:
        return None

def create_playerteam(player, team, active):
    logger.info('Adding %s to %s. Player active: %s' % (player, team, str(active)))
    return PlayerTeam.objects.create(player=player, team=team, active=active)

def create_show(title, blurb, start_date, active):
    logger.info('Adding %s show on %s. Active: %s' % (title, start_date, str(active)))
    return Show.objects.create(title=title, 
                               blurb=blurb, 
                               start_date=start_date, 
                               active=active)

def create_showphoto(team, show, photo):
    logger.info('Adding %s showphoto for %s to %s.' % (photo, team, show))
    return ShowPhoto.objects.create(team=team, show=show, photo=photo)

def create_teamcalendar(show, team, start_time, end_time):
    logger.info('Adding teamcalendar for %s to %s.' % (team, show))
    return TeamCalendar.objects.create(show=show,
                                       team=team,
                                       start_time=start_time,
                                       end_time=end_time)

if __name__ == "__main__":
    create_dev_db(log=True)
    logger.info('==> Done loading dev data')