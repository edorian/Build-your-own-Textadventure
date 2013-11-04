#!/usr/bin/env python
import os
import sys

project_root = os.path.dirname(os.path.abspath(__file__))


def setup_virtualenv():
    # activate virtualenv
    activate_this = os.path.join(project_root, '.env', 'bin', 'activate_this.py')
    execfile(activate_this, dict(__file__=activate_this))


def setup_pythonpath():
    # add src/ to python path
    sys.path.insert(0, os.path.join(project_root, 'src'))


def setup_django_settings():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")


def setup():
    setup_virtualenv()
    setup_pythonpath()
    setup_django_settings()


if __name__ == '__main__':
    setup()
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

