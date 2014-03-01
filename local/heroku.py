import psycopg2


def update_local_db_with_qsic27_production():
    performers = []
    groups = []
    group_performer_relationships = []
    with psycopg2.connect("dbname=qsic27_production") as conn_qsic27, conn_qsic27.cursor() as cur:
        # get players
        cur.execute("SELECT * FROM players_player;")
        for row in cur.fetchall():
            performers.append(convert_performer_row(row))

        # get teams
        cur.execute("SELECT * FROM teams_team;")
        for row in cur.fetchall():
            groups.append(convert_group_row(row))

        # get team_player relationships
        cur.execute("SELECT * FROM teams_playerteam;")
        for row in cur.fetchall():
            group_performer_relationships.append(convert_group_performer_relationship(row))

    with psycopg2.connect("dbname=qsic") as conn, conn.cursor() as cur:
        # add players
        pass
        # add groups

        # add performances


def convert_performer_row(row):
    """
    Convert player data to new db format
    """
    keys = ('id', 'first_name', 'last_name', 'improvteams_url', 'bio', 'h', 'u', 't')
    d = dict(zip(keys, row))
    print(d)


def convert_group_row(row):
    pass


def convert_group_performer_relationship(row):
    pass


def convert_performance_row(row):
    pass


def convert_team_performance_row(row):
    pass


if __name__ == '__main__':
    update_local_db_with_qsic27_production()