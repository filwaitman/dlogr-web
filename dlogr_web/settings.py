import os

import dj_database_url
import environ

from django.contrib import messages
from django.core.urlresolvers import reverse_lazy

env = environ.Env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DEBUG = env.bool('DJANGO_DEBUG', default=True)
if DEBUG:
    ALLOWED_HOSTS = []
    SECRET_KEY = 'itsdebugwhocares'

else:
    ALLOWED_HOSTS = ['dlogr.com', 'www.dlogr.com', 'localhost']
    SECRET_KEY = env('DJANGO_SECRET_KEY')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dlogr_web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dlogr_web.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'


########
# HEROKU
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

########
# CUSTOM
ROOT_DIR = environ.Path(__file__) - 2  # (/a/b/myfile.py - 2 = /a/)

INTERNAL_APPS = [
    'main',

]
INSTALLED_APPS += [
] + INTERNAL_APPS

DLOGR_BASE_API_URL = env('DLOGR_BASE_API_URL', default='https://api.dlogr.com')
LOGIN_URL = reverse_lazy('signin')

if 'main.utils.context_processor' not in TEMPLATES[0]['OPTIONS']['context_processors']:
    TEMPLATES[0]['OPTIONS']['context_processors'].append('main.utils.context_processor')

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

if env.bool('ROLLBAR_ENABLED', default=False):
    MIDDLEWARE = MIDDLEWARE + [  # pragma: no cover
        'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
    ]

    ROLLBAR = {  # pragma: no cover
        'access_token': env('ROLLBAR_ACCESS_TOKEN'),
        'environment': env('ENVIRONMENT_NAME'),
        'root': str(ROOT_DIR),
    }

if env.bool('FORCE_HTTPS', default=False):
    SECURE_SSL_REDIRECT = True  # pragma: no cover
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')  # pragma: no cover
