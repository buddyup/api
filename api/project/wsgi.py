"""
WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import sys
from sys import path

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
PROJECT_DIR = os.path.join(BASE_DIR, "project")
APPS_DIR = os.path.join(PROJECT_DIR, "apps")
path.insert(0, BASE_DIR)
path.insert(0, PROJECT_DIR)
path.insert(0, APPS_DIR)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.envs.live")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
