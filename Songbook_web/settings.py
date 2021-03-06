# -*- coding: utf-8 -*-
#    Copyright (C) 2014 The Songbook Team
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Django settings for Songbook-web project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(PROJECT_ROOT, ...)
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))


SECRET_KEY = 'minimal'

APPEND_SLASH = False

EMAIL_SUBJECT_PREFIX = '[Songbook Web]'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
)
INSTALLED_APPS += (
    'south',
    'background_task',
)
INSTALLED_APPS += (
    'generator',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'Songbook_web.urls'
SITE_ID = 1


WSGI_APPLICATION = 'Songbook_web.wsgi.application'


AUTHENTICATION_BACKENDS = (
    'generator.backends.EmailAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'db.sqlite3'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'ATOMIC_REQUESTS': True,
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True

gettext = lambda x: x

LANGUAGES = (
('fr', gettext('French')),
('en', gettext('English')),)


STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATIC_URL = '/data/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, "generator", "static"),
)

MEDIA_URL = '/medias/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "medias")

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Templates dans le dossier template
TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, 'templates/'),)

TEMPLATE_CONTEXT_PROCESSORS = (
        "django.contrib.auth.context_processors.auth",
        "django.core.context_processors.debug",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.core.context_processors.static",
        "django.core.context_processors.request",
        "django.core.context_processors.tz",
        "django.contrib.messages.context_processors.messages",
        )

LOGIN_URL = '/user/login'
LOGIN_REDIRECT_URL = '/user/'

SOUTH_TESTS_MIGRATE = False

from datetime import timedelta

# PDF cleaning settings
SONGBOOK_DELETE_POLICY = {"mode": "time",  # or "user" or "total_number"
                          "expiration_time": timedelta(weeks=1),
                          # "number": -1
                          }

try:
    from local_settings import *
except ImportError:
    pass
