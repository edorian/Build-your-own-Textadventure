# -*- coding: utf-8 -*-
from default_settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    
)
MANAGERS = ADMINS

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '<REPLACE:SECRET_KEY>'

MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
