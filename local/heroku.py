import datetime
import psycopg2
import sys

from django.template.defaultfilters import slugify
from django.utils import timezone

from qsic.parsers.improvteams.parser import ItPerformerParser
from qsic.parsers.improvteams.parser import ItTeamParser


def update_local_db_with_qsic27_production():
    data = {}
    with psycopg2.connect("dbname=qsic27_production") as conn_qsic27, conn_qsic27.cursor() as cur:

        # get players
        performers = {}
        cur.execute("SELECT * FROM players_player;")
        for row in cur.fetchall():
            performers.update(convert_performer_row(row))
        data.update({'performers': performers})

        # get shows
        events = {}
        cur.execute("SELECT * FROM shows_show;")
        for row in cur.fetchall():
            events.update(convert_event_row(row))
        data.update({'events': events})

        # get shows_teamcalendar
        group_performances = {}
        cur.execute("SELECT * FROM shows_teamcalendar;")
        for row in cur.fetchall():
            group_performances.update(convert_team_performance_row(row))
        data.update({'group_performances': group_performances})

        # get team_player relationships
        group_performer_relationships = {}
        cur.execute("SELECT * FROM teams_playerteam;")
        for row in cur.fetchall():
            group_performer_relationships.update(convert_group_performer_relationship_row(row))
        data.update({'group_performer_relationships': group_performer_relationships})

        # get teams_team
        groups = {}
        cur.execute("SELECT * FROM teams_team;")
        for row in cur.fetchall():
            groups.update(convert_group_row(row))
        data.update({'groups': groups})

    with psycopg2.connect("dbname=qsic") as conn, conn.cursor() as cur:
        # wipe all tables clean
        cur.execute("TRUNCATE qsic_event, qsic_group, qsic_groupperformerrelation, "
                    "qsic_performance, qsic_performancegroupperformerrelation, qsic_performer "
                    "CASCADE;")

        # add performers
        for p in data['performers'].values():
            cur.execute("INSERT INTO qsic_performer "
                        "(id, first_name, last_name, slug, it_url, it_id, bio) "
                        "VALUES "
                        "(%s, %s, %s, %s, %s, %s, %s)",
                        (p['id'],
                         p['first_name'],
                         p['last_name'],
                         p['slug'],
                         p['it_url'],
                         p['it_id'],
                         p['bio']))
        next_id = max([o['id'] for o in data['performers'].values()]) + 1
        cur.execute("ALTER SEQUENCE qsic_performer_id_seq RESTART WITH %s;", (next_id,))

        # add groups
        for g in data['groups'].values():
            cur.execute("INSERT INTO qsic_group "
                        "(id, name, slug, it_url, bio, create_dt, is_house_team) "
                        "VALUES "
                        "(%s, %s, %s, %s, %s, %s, %s)",
                        (g['id'],
                         g['name'],
                         g['slug'],
                         g['it_url'],
                         g['profile'],
                         g['created'],
                         g['is_house_team']))
        next_id = max([o['id'] for o in data['groups'].values()]) + 1
        cur.execute("ALTER SEQUENCE qsic_group_id_seq RESTART WITH %s;", (next_id,))

        # add group perofrmer relations
        for gpr in data['group_performer_relationships'].values():
            p = data['performers'][gpr['player_id']]
            g = data['groups'][gpr['team_id']]
            d = get_group_performer_relation(p, g, gpr['active'])
            cur.execute("INSERT INTO qsic_groupperformerrelation "
                        "(group_id, performer_id, start_dt, end_dt) "
                        "VALUES "
                        "(%s, %s, %s, %s)",
                        (d['group_id'],
                         d['performer_id'],
                         d['start_dt'],
                         d['end_dt']))
        next_id = max([o['id'] for o in data['group_performer_relationships'].values()]) + 1
        cur.execute("ALTER SEQUENCE qsic_groupperformerrelation_id_seq RESTART WITH %s;",
                    (next_id,))

        # add events
        for e in data['events'].values():
            performances = [p for p in data['group_performances'].values()
                            if p['show_id'] == e['id']]
            start_dt, end_dt = get_event_time_boundaries(e, performances)
            cur.execute("INSERT INTO qsic_event "
                        "(id, name, description, slug, _start_dt, _end_dt) "
                        "VALUES "
                        "(%s, %s, %s, %s, %s, %s)",
                        (e['id'],
                         e['title'],
                         e['blurb'],
                         e['slug'],
                         start_dt,
                         end_dt))
        next_id = max([o['id'] for o in data['events'].values()]) + 1
        cur.execute("ALTER SEQUENCE qsic_event_id_seq RESTART WITH %s;", (next_id,))

        # add performaces
        for p in data['group_performances'].values():
            name_ = data['groups'][p['team_id']]['name']
            slug = slugify(name_)
            event_start_dt = data['events'][p['event_id']]['start_date']
            start_dt = datetime.datetime.combine(event_start_dt, p['start_dt'])
            end_dt = datetime.datetime.combine(event_start_dt, p['end_dt'])

            cur.execute("INSERT INTO qsic_performance "
                        "(id, event_id, name, start_dt, end_dt, slug) "
                        "VALUES "
                        "(%s, %s, %s, %s, %s, %s)",
                        (p['id'],
                         p['event_id'],
                         name_,
                         start_dt,
                         end_dt,
                         slug))
        next_id = max([o['id'] for o in data['group_performances'].values()]) + 1
        cur.execute("ALTER SEQUENCE qsic_performance_id_seq RESTART WITH %s;", (next_id,))

        # add group performance relations
        for p in data['group_performances'].values():
            cur.execute("INSERT INTO qsic_performancegroupperformerrelation "
                        "(performance_id, performer_id, group_id) "
                        "VALUES "
                        "(%s, %s, %s)",
                        (p['id'],
                         None,
                         p['team_id']))


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
    return {d['id']: d}


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
        'slug': slug,
    })
    return {d['id']: d}


def convert_group_performer_relationship_row(row):
    """
    Convert group performer relationship
    """
    keys = ('id', 'player_id', 'team_id', 'active')
    d = dict(zip(keys, row))
    return {d['id']: d}


def get_group_performer_relation(performer, group, status):
    """
    Return dictionary in new db format with keys
    group_id, performer_id, start_dt, end_dt
    """
    d = {'performer_id': performer['id'], 'group_id': group['id']}

    # start_dt
    d['start_dt'] = group['created']

    # end_dt
    if status:
        # user is still active so don't add an `end_dt`
        d['end_dt'] = None
    else:
        # user is not active
        # if team is retired use team retire date as `end_dt` else
        d['end_dt'] = group['retired'] if group['retired'] else timezone.now()

    return d


def convert_event_row(row):
    """
    Convert show to event
    """
    keys = ('id', 'blurb', 'start_date', 'active', 'title')
    d = dict(zip(keys, row))
    d.update({'slug': slugify(d['title'])})
    return {d['id']: d}


def get_event_time_boundaries(event, performances):
    """
    Return start and end times for event based on performances within event
    """
    performances.sort(key=lambda p: p['start_time'])
    event_date = event['start_date']
    if performances:
        start_dt = timezone.datetime.combine(event_date, performances[0]['start_time'])
        end_dt = timezone.datetime.combine(event_date, performances[-1]['end_time'])
    else:
        start_dt = timezone.datetime.combine(event_date, datetime.time())
        start_dt = start_dt.replace(tzinfo=timezone.utc)
        end_dt = start_dt.replace(hour=23, minute=59, second=59)
    return start_dt, end_dt


def convert_team_performance_row(row):
    """
    Convert team performance to peroformance
    """
    keys = ('id', 'show_id', 'team_id', 'start_time', 'end_time')
    d = dict(zip(keys, row))
    d.update({
        'event_id': d['show_id'],
        'start_dt': d['start_time'],
        'end_dt': d['end_time']
    })
    return {d['id']: d}


if __name__ == '__main__':
    update_local_db_with_qsic27_production()