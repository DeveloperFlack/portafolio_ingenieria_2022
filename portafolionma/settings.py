"""
Django settings for portafolionma project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-&81wjre%bjk_rp_p%=vas!5v1bo9-2h+2=_=q)a3ju$$-@9^1t"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.dashboard",
    "apps.dashboard.controllers.modulos",
    "apps.dashboard.controllers.roles",
    "apps.dashboard.controllers.usuarios",
    "apps.dashboard.controllers.accidentes",
    "apps.dashboard.controllers.capacitaciones",
    "apps.dashboard.controllers.clientes",
    "apps.home",
    "apps.home.controllers.cliente",
    "apps.home.controllers.profesional",
    
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "portafolionma.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
                    "apps/dashboard/templates", "apps/home/templates",
                    "apps/dashboard/controllers/modulos/templates",
                    "apps/dashboard/controllers/usuarios/templates",
                    "apps/dashboard/controllers/roles/templates",
                    "apps/dashboard/controllers/clientes/templates",
                    "apps/dashboard/controllers/solicitudes/templates",
                    "apps/dashboard/controllers/capacitaciones/templates",
                    "apps/dashboard/controllers/asesorias/templates",
                    "apps/dashboard/controllers/accidentes/templates",
                    "apps/home/controllers/profesional/templates",
                    "apps/home/controllers/cliente/templates",
                 ],
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

WSGI_APPLICATION = "portafolionma.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator", },
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator", },
]
import platform

if (platform.system() ==  "Linux"):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'portafolionma1',
            'USER': 'portafolionma',
            'PASSWORD': 'Duoc.2022.1234',
            'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
            'PORT': '3306',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'portafolionma1',
            'USER': 'portafolionma',
            'PASSWORD': 'Duoc.2022.1234',
            'HOST': '3.95.197.48',   # Or an IP Address that your DB is hosted on
            'PORT': '3306',
        }
    }
# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "es-Cl"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


if (DEBUG == True):
    STATIC_URL = "stcs/"
    MEDIA_URL = '/media/'
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'apps', 'stcs'),
        os.path.join(BASE_DIR, 'apps/media')
    ]
    MEDIA_ROOT = os.path.join(BASE_DIR, "apps/stcs")
    
    x = platform.system()
    print ("Sistema Operativo", x)
    if (x ==  "Linux"):
        DB_HOST = 'localhost'
        DB_USER = 'portafolionma'
        DB_PASS = 'Duoc.2022.1234'
        DB_SCHEMA = 'portafolionma1'
    else:
        DB_HOST = '3.95.197.48'
        DB_USER = 'portafolionma'
        DB_PASS = 'Duoc.2022.1234'
        DB_SCHEMA = 'portafolionma1'

else:
    STATIC_URL = "stcs/"
    STATICFILES_ROOT = ['/home/ubuntu/portafolio_ingenieria_2022/apps/stcs', 'home/ubuntu/portafolio_ingenieria_2022/apps/stcs']
    MEDIA_URL = '/media/'
    MEDIA_ROOT = 'C:/Users/slaas/Desktop/duoc/portafolionma/apps/media'
    
    x = platform.system()
    print ("Sistema Operativo", x)
    if (x ==  "Linux"):
        DB_HOST = 'localhost'
        DB_USER = 'portafolionma'
        DB_PASS = 'Duoc.2022.1234'
        DB_SCHEMA = 'portafolionma1'
    else:
        DB_HOST = '3.95.197.48'
        DB_USER = 'portafolionma'
        DB_PASS = 'Duoc.2022.1234'
        DB_SCHEMA = 'portafolionma1'
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
