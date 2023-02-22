"""
Django settings for circle project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import sys
reload(sys)
sys.setdefaultencoding('UTF8')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'm47ij8d^&7wros!6%uorgsd*^v-8e!+rqyw1064d)eo(%$7jko'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#GCM_KEY = 'AIzaSyBtwk6drg-sH5eEK01x7pJElr6ylN91ZT0'
#GCM_KEY = 'AIzaSyDOwTCSGxzgjg3PvrkK7C1w_YSr185qUik' #440676984716 - old GCM key

GCM_KEY = 'AAAAMw7B05k:APA91bEItwqWu2SHDSBO28M6s94UXWv5BQ6eVQE0xBBvfgMmBgQH304g2EmnG65OYuiZkDDq_F5K_J-XPxjBl8xGM2iS8lSPhXFJdvveQIPM9MLIgyur5NYP6rsbav5nEu5G10T-dmPN' #219290915737

ECB_REST_AUTH_TOKEN = "x123"

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admindocs',
    'core_manager',
    'apis.android_api',
    'chama',
    'promotions',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',   
    'sorl.thumbnail',
    'sorl_thumbnail_serializer',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}

ROOT_URLCONF = 'circle.urls'

WSGI_APPLICATION = 'circle.wsgi.application'

AUTH_USER_MODEL = 'core_manager.User'

AUTHENTICATION_BACKENDS = (
    'apis.android_api.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db_circle.sqlite3'),
    }
} """



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'circle',
        'USER': 'root',
        'PASSWORD': 'r00t',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    },
    'local': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'chama',
        'USER': 'chama_test',
        'PASSWORD': 'ohl8Mae3ho',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.core.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        } 
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_L10N = True

USE_TZ = True


SUIT_CONFIG = {
    'ADMIN_NAME': 'Circle Manager',
    'SEARCH_URL': '/admin/search_all/',

    'MENU_ICONS': {
        'auth': 'icon-lock',
     },
    'MENU_EXCLUDE': ('authtoken', ),
    'LIST_PER_PAGE': 30,
    'SHOW_REQUIRED_ASTERISK': True,

    

    'MENU': (
        '-',
        {'label': 'Circle Management', 'permissions': 'chama', 'models': [
            {'label': 'Circle Accounts', 'url': 'chama.chamaaccount', 'permissions': ('auth.add_user', )},
            {'label': 'Circle Memberships', 'url': 'chama.chamamembership', 'permissions': ('auth.add_group', )},
            {'label': 'Circle Invitations', 'url': 'chama.chamainvitations', 'permissions': ('auth.add_group', )},
            {'label': 'Circle Member Approvals', 'url': 'chama.memberappprovals', 'permissions': ('auth.add_group', )},
            {'label': 'Closed Circles', 'url': 'chama.closedcircles', 'permissions': ('auth.add_group', )},
        ]},
        {'label': 'System Setup', 'permissions': 'chama', 'models': [
            {'label': 'Comissions Table', 'url': 'core_manager.commisiontable', 'permissions': ('auth.add_user', )},
            {'label': 'Currencies', 'url': 'core_manager.circlecurrency', 'permissions': ('auth.add_user', )},
            {'label': 'Payment Accounts', 'url': 'core_manager.paymentaccount', 'permissions': ('auth.add_user', )},
        ]},
        {'label': 'Promotions', 'permissions': 'chama', 'models': [
            {'label': 'Promotions', 'url': 'promotions.promotion', 'permissions': ('auth.add_user', )},
            {'label': 'Promotion Bonus', 'url': 'promotions.promotionbonus', 'permissions': ('auth.add_user', )},
        ]},
        {'label': 'Payments', 'permissions': 'chama', 'models': [
            {'label': 'Circle Contributions', 'url': 'chama.chamacontributions', 'permissions': ('auth.add_group', )},
            {'label': 'Incoming Payments', 'url': 'core_manager.incomingpayments', 'permissions': ('auth.add_user', )},
            {'label': 'Invoices', 'url': 'chama.invoices', 'permissions': ('auth.add_user', )},
            {'label': 'Unpaid Invoices', 'url': 'chama.unpaidinvoices', 'permissions': ('auth.add_user', )},

            {'label': 'Survey List', 'url': 'chama.surveylist', 'permissions': ('auth.add_user', )},
            {'label': 'Notice List', 'url': 'chama.noticelist', 'permissions': ('auth.add_user', )},
            {'label': 'Inactive Memberships', 'url': 'chama.inactivemembership', 'permissions': ('auth.add_user', )},
            {'label': 'Card Payment Requests', 'url': 'core_manager.cardpaymentrequests', 'permissions': ('auth.add_user', )},
            {'label': 'Client Cards', 'url': 'core_manager.clientcard', 'permissions': ('auth.add_user', )},
            
            {'label': 'PesaPal Transactions', 'url': 'core_manager.pesapaltransactions', 'permissions': ('auth.add_user', )},
            {'label': 'PesaPal Transaction Users', 'url': 'core_manager.pesapaltransactionusers', 'permissions': ('auth.add_user', )},
        ]},
        
        {'label': 'CommTool', 'permissions': 'chama', 'models': [
            {'label': 'Android Notifications', 'url': 'chama.chamanotifications', 'permissions': ('auth.add_group', )},
            {'label': 'Circle E-mails', 'url': 'chama.chamaemails', 'permissions': ('auth.add_group', )},
            {'label': 'Notification Log', 'url': 'chama.notificationlog', 'permissions': ('auth.add_group', )},
        ]},

        # Separator
        '-',

        # Custom app and model with permissions
        {'label': 'Authorization', 'permissions': 'auth.add_user', 'models': [
            {'label': 'User Accounts', 'url': 'core_manager.user', 'permissions': ('auth.add_user', )},
            {'label': 'User Groups', 'url': 'auth.group', 'permissions': ('auth.add_group', )}
        ]},
    )

}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static/")


STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, "assets/"),
)

# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media/')


# URL that handles the media served from MEDIA_ROOT. Make sure to use a trailing slash.
MEDIA_URL = '/media/'

THUMBNAIL_DEBUG = True

OLD_PASSWORD_FIELD_ENABLED = True
LOGOUT_ON_PASSWORD_CHANGE = True

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'circle@imaginarium.co.ke'
EMAIL_HOST_PASSWORD = 'Circlehelp19!'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'circle@imaginarium.co.ke'
ADMINS = [('Michael', 'micmukima@gmail.com'), ('Talend', 'info@talend.co.ke')]


LOGGING = {
    'version': 1,
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        }
    },
}

