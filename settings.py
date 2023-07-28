"""
Django settings for si-django-com-oracle-da-anav2 project.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import environ
import yaml
from pathlib import Path

# Don't generate translations for this file, import as _gettext_lazy
from django.utils.translation import gettext_lazy as _gettext_lazy

from . import __version__

# Raise an exception when accessing an undefined variable
class InvalidString(str):
    def __mod__(self, other):
        from django.template.base import TemplateSyntaxError
        raise TemplateSyntaxError(f'Undefined variable or unknown value for: {other}')

env = environ.Env()

# Raíz da estrutura do projeto.
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# User Custom da aplicação.
AUTH_USER_MODEL = 'core.User'


if env.bool('LOAD_DOTENV', True):
    environ.Env.read_env(ROOT_DIR / '.env')

PROJECT_BASE_DIR = Path(env.str('PROJECT_BASE_DIR', default='')).resolve()  # Pasta onde é para criar as pastas /static e /media
SECRET_KEY = env('DJANGO_SECRET_KEY')  # SECURITY WARNING: keep the secret key used in production secret!
DEBUG = env.bool('DEBUG', default=False)  # SECURITY WARNING: don't run with debug turned on in production!
LOCAL_LOG_LEVEL = env.str('LOCAL_LOG_LEVEL', default='DEBUG')  # Nível dos loggers.
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
INTERNAL_IPS = env.list('INTERNAL_IPS', default=[])
PROJECT_NAME = 'si-django-com-oracle-da-anav2'
APP_VERSION = __version__

# Configurações relacionadas com rotas.
# SCRIPT_NAME é uma variável de ambiente que o gunicorn utiliza para adcionar ao inicio de todos os URLs, e o Django também a processa nos reverses() de forma automática,
# (ver https://docs.djangoproject.com/en/3.2/_modules/django/urls/base/#reverse). Apenas deve estar definida quando se usa gunicorn.
SCRIPT_NAME = env.str('SCRIPT_NAME', '')  # Usar apenas com gunicorn, deve incluir a partícula que identifica o projeto.
BASE_API_URL = env.str('BASE_API_URL', '')  # Sub-endereço para a API.

# Application definition
ROOT_URLCONF = 'uporto.django_com_oracle_da_anav2.urls'

INSTALLED_APPS = [
    'uporto.django_com_oracle_da_anav2.core',
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
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configurações relativas aos templates.
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
            'string_if_invalid': InvalidString('%s'),
        },
    },
]

# Logging.
# Evitar configurações "especiais", ver https://note.uporto.pt/display/DIP/Logging para mais informação.
LOGGING_CONF_FILE = env.str('LOGGING_CONF_FILE', '')
if LOGGING_CONF_FILE:  # Configuração por ficheiro YAML.
    with open(LOGGING_CONF_FILE) as fd:
        conf = yaml.safe_load(fd)
    LOGGING = conf
else:  # Configuração local, apenas usada durante do desenvolvimento.
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d DEMO_POSTGRESQL %(message)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            },
        },
        'root': {'level': LOCAL_LOG_LEVEL, 'handlers': ['console']},
        'loggers': {
            'uporto.demo_postgresql': {
                'handlers': ['console'],
                'level': LOCAL_LOG_LEVEL,
                'propagate': False,
            },
        },
    }

WSGI_APPLICATION = 'uporto.django_com_oracle_da_anav2.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = 'pt-pt'
LANGUAGES = [
    ('pt', _gettext_lazy('Portuguese')),
    ('en', _gettext_lazy('English')),
]
TIME_ZONE = 'Europe/Lisbon'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = 'static/'
STATIC_ROOT = PROJECT_BASE_DIR / '/static'  # Hardcoded para tentar uma coerência entre os vários projetos.
MEDIA_URL = 'media/'
MEDIA_ROOT = PROJECT_BASE_DIR / '/media'  # Hardcoded para tentar uma coerência entre os vários projetos.

# Configurações para DEBUG apenas (necessário para o DjangoToolbar).
if DEBUG:
    import mimetypes

    INSTALLED_APPS += [
        'django_extensions',
        'debug_toolbar',
    ]
    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ] + MIDDLEWARE

    mimetypes.add_type("application/javascript", ".js", True)

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }


print('Ficheiro \x1b[33msettings.py\x1b[0m lido. Modo debug está \x1b[35m' + str(DEBUG) + '\x1b[0m.')
print('\x1b[33mSCRIPT_NAME\x1b[0m: \x1b[35m' + SCRIPT_NAME + '\x1b[0m')
print('\x1b[33mALLOWED_HOSTS\x1b[0m: \x1b[35m' + str(ALLOWED_HOSTS) + '\x1b[0m')
