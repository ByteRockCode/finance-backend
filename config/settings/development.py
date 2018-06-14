# flake8: noqa: F405

from .base import *


ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(' ')
DEBUG = True
SECRET_KEY = 'i_am_a_super_secret_key'

INSTALLED_APPS += [
    'django_extensions',
]

if os.environ.get('DEBUG_TOOLBAR', False):
    INSTALLED_APPS += [
        'debug_toolbar',
    ]

    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]
