# -*- coding: utf-8 -*-
import os
import subprocess
from fabric.api import abort, cd, local, env, run, settings, sudo


services = ('txtadv-website',)

project_name = 'txtadv'
path = '/srv/%s/' % project_name

config = {
    'path': path,
    'project': project_name,
}


def setup_virtualenv():
    '''
    * setup virtualenv
    '''
    with cd(path):
        run('virtualenv .env --prompt="(%s)" --system-site-packages' % config['project'])

def pip_install():
    '''
    * install dependcies
    '''
    with cd(path):
        run('.env/bin/pip install -r requirements/common.txt --upgrade')

def migrate():
    '''
    * run syncdb
    * run migrate
    '''
    with cd(path):
        run('python manage.py syncdb --migrate --noinput')

def start():
    '''
    * start all services
    '''
    for service in services:
        sudo('start %s' % service)

def stop():
    '''
    * stop all services
    '''
    for service in services:
        sudo('stop %s' % service)

def restart():
    '''
    * restart all services
    '''
    for service in services:
        sudo('restart %s' % service)

def status():
    '''
    * show if services are running
    '''
    with settings(warn_only=True):
        for service in services:
            sudo('status %s' % service)

def reload_webserver():
    '''
    * reload nginx
    '''
    sudo('/etc/init.d/nginx reload')

def restart_webserver():
    '''
    * restart nginx
    '''
    sudo('/etc/init.d/nginx restart')

def pull():
    '''
    * git pull on the server
    '''
    with cd(path):
        run('git fetch origin')
        run('git reset --hard origin/master')

def deploy(pip_install=True):
    '''
    * update source
    * run pip install on server and run db migrations
    * restart services
    '''
    pull()
    if pip_install not in (False, 0, 'False', '0'):
        pip_install()
    migrate()
    restart()
