import psycopg2
import sys

from django.template.defaultfilters import slugify

from qsic.parsers.improvteams.parser import ItPerformerParser
from qsic.parsers.improvteams.parser import ItTeamParser


def update_local_db_with_qsic27_production():
    performers = []
    groups = []
    group_performer_relationships = []
    with psycopg2.connect("dbname=qsic27_production") as conn_qsic27, conn_qsic27.cursor() as cur:
        # get players
        cur.execute("SELECT * FROM players_player;")
        for row in cur.fetchall():
            performers.append(convert_performer_row(row))

        # get shows
        cur.execute("SELECT * FROM shows_show;")

        # get shows_teamcalendar
        cur.execute("SELECT * FROM shows_teamcalendar;")

        # get team_player relationships
        cur.execute("SELECT * FROM teams_playerteam;")
        for row in cur.fetchall():
            group_performer_relationships.append(convert_group_performer_relationship(row))

        # get teams_team
        cur.execute("SELECT * FROM teams_team;")
        for row in cur.fetchall():
            groups.append(convert_group_row(row))

    with psycopg2.connect("dbname=qsic") as conn, conn.cursor() as cur:
        # add players
        pass
        # add groups
        pass
        # add performances
        pass


def convert_performer_row(row):
    """
    Convert player data to new db format
    """
    keys = ('id', 'first_name', 'last_name', 'improvteams_url', 'bio', 'h', 'u', 't')
    d = dict(zip(keys, row))
    parser = ItPerformerParser()
    parser.url = d.pop('improvteams_url', '')
    parser.parse_it_id_from_url()
    slug = slugify(' '.join((d['first_name'], d['last_name'])))
    d.update({
        'it_id': parser.it_id,
        'it_url': parser.url,
        'slug': slug
    })
    return d


def convert_group_row(row):
    """
    Convert group data to new db format
    """
    keys = ('id', 'name', 'created', 'retired', 'team_logo', 'team_photo', 'website',
            'logo_slice', 'improvteams_url', 'profile', 'name_color', 'name_shadow_color',
            'is_house_team', 'background_color')
    d = dict(zip(keys, row))
    slug = slugify(d['name'])
    url = d['improvteams_url'] if 'improvteams.com' in d['improvteams_url'] else ''
    d.update({
        'it_url': url,
        'slug': slug
    })
    return d


def convert_group_performer_relationship(row):
    """
    Convert performer
    """
    keys = ('id', 'player_id', 'team_id', 'active')
    d = dict(zip(keys, row))
    pass


def convert_performance_row(row):
    k = ('id', 'blurb', 'start_date', 'active', 'title')
    d = dict(zip(keys, row))
    pass


def convert_team_performance_row(row):
    k = ('id', 'show_id', 'team_id', 'start_time', 'end_time')
    d = dict(zip(keys, row))
    pass


if __name__ == '__main__':
    update_local_db_with_qsic27_production()