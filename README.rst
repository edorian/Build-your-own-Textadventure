Pre-Requirements
================

Python dependencies are handled with buildout and the installation is
described below. The project still needs some non-python libraries to work.
Please install them by using your system's package manager:

* graphviz
* pygraphviz

If you use Ubuntu you can execute the following command to install the
dependencies::

    sudo apt-get install graphviz python-pygraphviz

Setting things up
=================

To install the site do the standard buildout thing::

    python bootstrap.py
    bin/buildout
    bin/django syncdb
    bin/django migrate

To setup demo Data including a User (demo/demo) and some example Adventures
please use::

    bin/django loaddata auth adventure

Then you have the ``django-admin.py`` wrapper at ``bin/django``. To run the
development server, do ``bin/django runserver``.
