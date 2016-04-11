#!/usr/bin/env python
import os
import sys
from sys import path

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
PROJECT_DIR = os.path.join(BASE_DIR, "project")
APPS_DIR = os.path.join(PROJECT_DIR, "apps")
path.insert(0, BASE_DIR)
path.insert(0, PROJECT_DIR)
path.insert(0, APPS_DIR)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
