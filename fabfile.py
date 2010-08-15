# -*- coding: utf-8 -*-
import os
import subprocess
from fabric.api import abort, cd, local, env, run, settings, sudo


services = ('txtadv-gunicorn',)

project_name = 'txtadv'
path = '/srv/%s/' % project_name

config = {
    'path': path,
    'project': project_name,
}


def test():
    '''
    * test project and abort if tests have failed
    '''
    if subprocess.call(['bin/test'], shell=True) != 0:
        abort('tests failed.')

def bootstrap():
    with cd(path):
        run('python bootstrap.py')

def buildout():
    '''
    * run a buildout
    '''
    with cd(path):
        run('test -e bin/buildout || python bootstrap.py')
        run('bin/buildout')

def migrate():
    '''
    * run syncdb
    * run migrate
    '''
    run('%sbin/django syncdb' % path)
    run('%sbin/django migrate' % path)

def start():
    '''
    * start all services
    '''
    for service in services:
        sudo('svc -u /etc/service/%s' % service)

def stop():
    '''
    * stop all services
    '''
    for service in services:
        sudo('svc -d /etc/service/%s' % service)

def restart():
    '''
    * restart all services
    '''
    for service in services:
        sudo('svc -du /etc/service/%s' % service)

def status():
    '''
    * show if services are running
    '''
    with settings(warn_only=True):
        for service in services:
            sudo('svstat /etc/service/%s' % service)

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
        run('git pull')

def deploy(run_buildout=True):
    '''
    * test project
    * upload source
    * run buildout on server and run db migrations
    * restart services
    '''
    test()
    pull()
    if run_buildout not in (False, 0, 'False', '0'):
        buildout()
    migrate()
    restart()
