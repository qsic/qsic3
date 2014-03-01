# TODO port this to python3
from fabric.api import local


def copy_db_prod_to_staging(prod_app='qsic-production',
                            staging_app='qsic-staging'):
    """
    Copy production database from prod_app to staging database
    in staging_app
    """

    # Capture a snapshot of the source database
    #
    # The --expire flag tells pgbackups to automatically expire the
    # oldest manual backup if the retention limit is reached.
    cmd = ('heroku pgbackups:capture -a %(source_app)s --expire' %
           {'source_app': prod_app})
    local(cmd)

    # Create backup of target app (staging app) database for easy
    # rollback.
    cmd = ('heroku pgbackups:capture -a %(target_app)s --expire' %
           {'target_app': staging_app})
    local(cmd)

    # Perform copy
    #
    # Restore the most recent backup of source-app to the database
    # located at psql_url where the color of the handle is the
    # color of the database handle on the target-app application.
    cmd = ('heroku pgbackups:restore %(psql_url)s -a %(target_app)s '
           '`heroku pgbackups:url -a %(source_app)s` '
           '--confirm %(target_app)s' %
           {'source_app': prod_app, 'target_app': staging_app,
            'psql_url': get_heroku_psql_url_name(staging_app)})
    local(cmd)


def get_heroku_psql_url_name(app):
    cmd = 'heroku config | grep HEROKU_POSTGRESQL'
    config_var = local(cmd, True)
    name = config_var.split(':')[0]
    return name


def collectstatic(heroku_app=None):
    if heroku_app:
        cmd = ('heroku run python manage.py collectstatic --noinput '
               '--app %(heroku_app)s' %
               {'heroku_app': heroku_app})
    else:
        cmd = 'python manage.py collectstatic --noinput'

    local(cmd)


def push(remote_branch=None, local_branch=None, heroku_app=None):
    if remote_branch and local_branch:
        cmd = ('git push %(remote_branch)s %(local_branch)s' %
               {'remote_branch': remote_branch, 'local_branch': local_branch})
        local(cmd)

    if heroku_app:
        collectstatic(heroku_app)


def push_to_github(local_branch='master'):
    cmd = ('git push origin %(local_branch)s' %
           {'local_branch': local_branch})
    local(cmd)


def push_to_staging():
    push(remote_branch='staging', local_branch='master',
         heroku_app='qsic-staging')


def push_to_production():
    push(remote_branch='production', local_branch='master',
         heroku_app='queens-secret')

