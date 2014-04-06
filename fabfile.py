"""
As of 2014-04-04, Fabric is not supported on python 3+. To
use this fabfile, call the functions in this file from
within a python 2.7 env.
"""
from fabric.api import local


def transfer_db(source_app='qsic-production', target_app='qsic-staging'):
    """
    Copy database from ``source_app`` to ``target_app``.
    """

    # Get HEROKU_POSTGRESQL url aliases.
    source_db_url = get_heroku_psql_url_name(source_app)
    target_db_url = get_heroku_psql_url_name(target_app)

    # Capture a snapshot of the source database
    #
    # The --expire flag tells pgbackups to automatically expire the
    # oldest manual backup if the retention limit is reached.
    cmd = 'heroku pgbackups:capture {source_db_url} --app {source_app} --expire'.format(**locals())
    local(cmd)

    # Create backup of target app (staging app) database for easy
    # rollback.
    cmd = 'heroku pgbackups:capture {target_db_url} --app {target_app} --expire'.format(**locals())
    local(cmd)

    # Perform transfer.
    cmd = ('heroku pgbackups:transfer {source_db_url} '
           '{target_app}::{target_db_url} '
           '--app {source_app} --confirm {source_app}'.format(**locals()))
    local(cmd)


def get_heroku_psql_url_name(app):
    """
    Pull Postgres DB URL alias (of the form HEROKU_POSTGRESQL.+) from heroku config.
    """
    cmd = 'heroku config --app {app} | grep HEROKU_POSTGRESQL'.format(app=app)
    config_var = local(cmd, True)
    name = config_var.split(':')[0]
    return name


def collectstatic(app):
    """
    Run collectstatic on ``app``.
    """
    cmd = 'heroku run python manage.py collectstatic --noinput --app {app}'.format(app=app)
    local(cmd)


def migrate(app):
    """
    Migrate database schema to latest South schemamigration.
    """
    cmd = 'heroku run python manage.py migrate --app {app}'.format(app=app)
    local(cmd)


def push(remote, local_branch, heroku_app=None):
    """
    Push branch ``local_branch`` up to ``remote`` via git.

    New branch on ``remote`` will be named ``local_branch``.
    """
    if remote and local_branch:
        cmd = ('git push {remote} {local_branch}'.format(**locals()))
        local(cmd)

    if heroku_app:
        collectstatic(heroku_app)


def pushto(app):
    """
    Push master branch in local git repo up to
    qsic app specified by ``app``.
    """
    push(app, 'master', heroku_app=app)
