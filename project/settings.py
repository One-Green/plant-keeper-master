"""
Django settings for project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from pathlib import Path
from tzlocal import get_localzone

__repo__ = "https://github.com/One-Green/core-api-gateway"
__version__ = "0.0.4"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "d#13myqgw8$g=*)z5zv0q^)^#kra!77mjtbg07zgada@pnmn0a"

# SECURITY WARNING: don't run with debug turned on in production!
if os.getenv("DEBUG").lower() == "true":
    DEBUG = True
    ALLOWED_HOSTS = ["*"]
elif os.getenv("DEBUG").lower() == "false":
    DEBUG = False
    ALLOWED_HOSTS = [
        os.getenv("ALLOWED_HOSTS"),
    ]
    CSRF_TRUSTED_ORIGINS = [
        os.getenv("CSRF_TRUSTED_ORIGINS"),
    ]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_filters",
    "drf_yasg",
    "glbl",
    "sprinkler",
    "water",
    "light",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("POSTGRES_DB", "postgres"),
        "USER": os.getenv("POSTGRES_USER", "postgres"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

SYSTEM_TIME_ZONE = get_localzone()

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# DRF
# use orjson renderer instead default json (faster)
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": (
        "drf_orjson_renderer.renderers.ORJSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}
# USER MODEL SETTING
AUTH_USER_MODEL = "accounts.CustomUser"

# CELERY + REDIS configuration
BROKER_URL = "redis://{0}:{1}".format(
    os.getenv("REDIS_HOST", "localhost"), os.getenv("REDIS_PORT", "6379")
)
CELERY_RESULT_BACKEND = "redis://{0}:{1}".format(
    os.getenv("REDIS_HOST", "localhost"), os.getenv("REDIS_PORT", "6379")
)
CELERY_ACCEPT_CONTENT = ["application/x-python-serialize"]
CELERY_TASK_SERIALIZER = "pickle"
CELERY_RESULT_SERIALIZER = "pickle"
CELERY_TIMEZONE = "UTC"

# MQTT configuration
MQTT_HOST: str = os.getenv("MQTT_HOST", "127.0.0.1")
MQTT_PORT: int = int(os.getenv("MQTT_PORT", 1883))
MQTT_USERNAME: str = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD: str = os.getenv("MQTT_PASSWORD")

# ########## SPRINKLER APP CONFIGURATION ##########
# SPRINKLERS TOPICS -------------------------------
MQTT_SPRINKLER_SENSOR_TOPIC: str = "sprinkler/sensor"
MQTT_SPRINKLER_CONTROLLER_TOPIC: str = "sprinkler/controller"
# WATER TOPICS ------------------------------------
MQTT_WATER_SENSOR_TOPIC: str = "water/sensor"
MQTT_WATER_CONTROLLER_TOPIC: str = "water/controller"
# LIGHT TOPICS ------------------------------------
MQTT_LIGHT_SENSOR_TOPIC: str = "light/sensor"
MQTT_LIGHT_CONTROLLER_TOPIC: str = "light/controller"

# Default values
DEFAULT_WATER_DEVICE = "tap-water"
