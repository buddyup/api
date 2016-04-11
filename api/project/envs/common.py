
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
from os.path import abspath, join, dirname
from sys import path
from envs.keys_and_passwords import *

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
PROJECT_DIR = os.path.join(BASE_DIR, "project")
APPS_DIR = os.path.join(PROJECT_DIR, "apps")


# From other app

ADMINS = (
    ('Steven Skoczen', 'steven@buddyup.org'),
)

MANAGERS = ADMINS
EMAIL_SUBJECT_PREFIX = "BuddyUp "
SERVER_EMAIL = 'BuddyUp Notifications<notifications@buddyup.org>'
DEFAULT_FROM_EMAIL = 'BuddyUp Notifications<notifications@buddyup.org>'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

ALLOWED_HOSTS = [
    "poc.buddyup.org",
    "buddyup-poc-staging.herokuapp.com",
    "buddyup-poc.herokuapp.com",
    "buddyup-poc.s3.amazonaws.com",
    "api.buddyup.org",
    "localhost",
    "api.bu.dev",
    "api.bu",
]

import djcelery
djcelery.setup_loader()
BROKER_URL = 'redis://localhost:6379/6'

# CELERYBEAT_SCHEDULE = {
#     'every-hour': {
#         # 'task': 'get_data',
#         # 'schedule': crontab(minute=1)
#     }
# }
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
CELERYD_TASK_TIME_LIMIT = 15
CELERY_ROUTES = {
    'events.tasks.sync_analytics': {'queue': 'analytics'},
    'events.tasks.sync_all_class_analytics': {'queue': 'analytics'},
    'events.tasks.sync_class_data': {'queue': 'analytics'},
    'events.tasks.sync_journey': {'queue': 'analytics'},
    'events.tasks.push_and_email': {'queue': 'push'},
    'events.tasks.start_push_timing': {'queue': 'push'},
    'events.tasks.end_push_timing': {'queue': 'push'},
    'events.tasks.log_event': {'queue': 'logging'},
    'events.tasks.encrypt_log': {'queue': 'logging'},
    'gatekeeper.tasks.log_signup_attempt': {'queue': 'logging'},
    'gatekeeper.tasks.log_delete_attempt': {'queue': 'logging'},
    'gatekeeper.tasks.log_access_attempt': {'queue': 'logging'},
    'gatekeeper.tasks.log_password_attempt': {'queue': 'logging'},

}

STATIC_ROOT = join(PROJECT_DIR, "collected_static")
STATIC_URL = '/static/'
MEDIA_URL = 'http://api.bu/media/'
MEDIA_ROOT = join(PROJECT_DIR, "media")


AWS_QUERYSTRING_AUTH = False
STATICFILES_EXCLUDED_APPS = []
COMPRESS_ROOT = STATIC_ROOT

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
GOOGLE_ANALYTICS_PROPERTY_ID = ""
# INTERCOM_API_KEY = os.environ["INTERCOM_API_KEY"]
if "WILL_URL" in os.environ:
    WILL_URL = os.environ["WILL_URL"]
else:
    WILL_URL = "http://localhost:8001"
IONIC_APP_ID = os.environ["IONIC_APP_ID"]
IONIC_KEY = os.environ["IONIC_KEY"]
IONIC_PRIVATE_KEY = os.environ["IONIC_PRIVATE_KEY"]
API_ENDPOINT = "http://localhost:8120"

APPFIGURES_CLIENT_KEY = os.environ.get("APPFIGURES_CLIENT_KEY", None)
APPFIGURES_SECRET_KEY = os.environ.get("APPFIGURES_SECRET_KEY", None)
APPFIGURES_USERNAME = os.environ.get("APPFIGURES_USERNAME", None)
APPFIGURES_PASSWORD = os.environ.get("APPFIGURES_PASSWORD", None)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
}
import logging
selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
selenium_logger.setLevel(logging.WARNING)
logging.getLogger().setLevel(logging.WARNING)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '67f6tqzi5#y+s5fbxq3zw)*!2#ta6n(mcd*-4%3n=lmtbkycl0'

if "ACCESS_LOG_KEY" not in os.environ:
    ACCESS_LOG_KEY = SECRET_KEY
else:
    ACCESS_LOG_KEY = os.environ["ACCESS_LOG_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'django_extensions',
    'django_nose',
    'djcelery',
    'djrill',

    'events',
    'gatekeeper',
    'utils',
)

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
)

ROOT_URLCONF = 'project.urls'
AUTH_USER_MODEL = 'gatekeeper.User'
if "FIREBASE_ENDPOINT" in os.environ:
    FIREBASE_ENDPOINT = os.environ["FIREBASE_ENDPOINT"]
else:
    FIREBASE_ENDPOINT = "https://buddyup-dev.firebaseio.com"

WSGI_APPLICATION = 'project.wsgi.application'

# SESSION_COOKIE_NAME = "buddyup_id_dev"
# SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
SESSION_SAVE_EVERY_REQUEST = True

CORS_ORIGIN_WHITELIST = (
    'buddyup.org',
    'localhost',
    'bu.dev',
)
# CORS_ALLOW_HEADERS = ('accept-encoding', )
# TODO: limit to proper, if possible (app,etc)
CORS_ORIGIN_ALLOW_ALL = True

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'buddyup',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}
if 'CIRCLECI' in os.environ:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'circle_test',
        'USER': 'ubuntu',
    }
if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

APPEND_SLASH = False
STATIC_URL = '/static/'


TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

ROLLBAR = {
    'access_token': os.environ["ROLLBAR_TOKEN"],
    'environment': 'development' if DEBUG else 'production',
    'branch': 'master',
    'root': BASE_DIR,
}
