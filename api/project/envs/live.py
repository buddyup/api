import os
from memcacheify import memcacheify
from postgresify import postgresify
from envs.common import *


DEBUG = False
TEMPLATE_DEBUG = DEBUG

SESSION_COOKIE_DOMAIN = "buddyup.org"
SESSION_COOKIE_NAME = "buddyup_id"
CORS_ORIGIN_WHITELIST = (
    'buddyup.org',
    'tng.buddyup.org',
    'localhost',
    'bu.dev',
)

# TODO: limit to proper, if possible (app,etc)
CORS_ORIGIN_ALLOW_ALL = True
# TODO: After https:
# SESSION_COOKIE_SECURE = True

EMAIL_BACKEND = 'django_ses_backend.SESBackend'

BROKER_URL = os.environ["REDISTOGO_URL"]

MEDIA_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
ADMIN_MEDIA_PREFIX = '%sadmin/' % STATIC_URL
COMPRESS_URL = STATIC_URL
FAVICON_URL = "%sfavicon.ico" % STATIC_URL
API_ENDPOINT = "https://api.buddyup.org"

CACHES = memcacheify()
DATABASES = None
DATABASES = postgresify()
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = "backends.CachedS3BotoStorage"
COMPRESS_STORAGE = STATICFILES_STORAGE

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
GOOGLE_ANALYTICS_PROPERTY_ID = ""
