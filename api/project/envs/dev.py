import os
from os.path import join
from envs.common import *

SESSION_COOKIE_DOMAIN = "app.bu"
ALLOWED_HOSTS = []

if 'CIRCLECI' not in os.environ:
    BROKER_URL = 'redis://redis:6379/6'

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
            'LOCATION': 'memcached:11211',
        }
    }


if False:
    MIDDLEWARE_CLASSES = (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ) + MIDDLEWARE_CLASSES

    INTERNAL_IPS = ('127.0.0.1',)

    INSTALLED_APPS += ("debug_toolbar", )
