"""
Django settings for NewsHund project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""


from pathlib import Path
from datetime import timedelta
import razorpay
import os
import stripe
import environ

# Load environment variables from .env file
env = environ.Env()
environ.Env.read_env() 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-nngf6l3$yc+qk965*flzv+u=+am5fmo5=#q4ntu!2*r-wia$-7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer",
            },
        
    }

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user_side',
    'rest_framework_simplejwt',
    'rest_framework',
    'rest_framework.authtoken',
    "rest_framework_simplejwt.token_blacklist",
    'pyotp',
    'corsheaders',
    'phonenumber_field',
    'django_cron',
    'stripe',
    'django_cleanup.apps.CleanupConfig',
]



MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Add this as the first middleware
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

CORS_ALLOWED_ORIGINS = env("CORS_ORIGINS", default="").split(",")



ROOT_URLCONF = 'NewsHund.urls'

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



WSGI_APPLICATION = 'NewsHund.wsgi.application'
ASGI_APPLICATION = 'NewsHund.asgi.application'



# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        
        'NAME': env('NAME'),           
        'USER': env('DBUSER'),      # Database user
        'PASSWORD': env('PASSWORD'),  # Database user's password
        'HOST': env('HOST'),  # Hostname or IP address of the PostgreSQL server
        'PORT': '',                  # Leave empty for default PostgreSQL port (5432)
    }
}



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    
    'DEFAULT_AUTHENTICATION_CLASSES': (
        
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
    
}

CRON_CLASSES = [
    # Other cron tasks...
    'user_side.cron.UpdateExpiredSubscriptions',
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT =os.path.join(BASE_DIR, '.static/assets')
MEDIA_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER=env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD=env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS=True


AUTH_USER_MODEL = 'user_side.User'

API_KEY = env('API_KEY')
RAZORPAY_SECRET_KEY = env('RAZORPAY_SECRET_KEY')

razorpay_client = razorpay.Client(auth=(API_KEY, RAZORPAY_SECRET_KEY))

stripe.api_key = 'sk_test_51NYMKpSC5bTWQxmddrBf1kVS9CTBcwpaRvfBrjKVikB7KeNIdFNXLfuWQFh3NE5TE0KCwIHPtzf6ZeO9qCQDd9Y9006KkDt31O' 


STRIPE_SECRET_KEY = 'sk_test_51NYMKpSC5bTWQxmddrBf1kVS9CTBcwpaRvfBrjKVikB7KeNIdFNXLfuWQFh3NE5TE0KCwIHPtzf6ZeO9qCQDd9Y9006KkDt31O'  # Replace with your Stripe secret key
STRIPE_PUBLIC_KEY = 'pk_test_51NYMKpSC5bTWQxmdX0tAI4oxyxQwofBkLLve0jCroJxsSGYGJYoRfgYbwQzRR9dQlvB0geCM7I2oxaI4GqY6mk9E008zJnUOzC'
STRIPE_PRICE_IDS = {
    'monthly': 'price_1NYMexSC5bTWQxmdFHhXhSTq',
    'six_months': 'price_1NYMexSC5bTWQxmd4MrogEZ5',
    'yearly': 'price_1NYMexSC5bTWQxmdEfODBwhw',
}
STRIPE_WEBHOOK_SECRET = 'whsec_XXXXXXXXXXXXXXXXXXXX'

# settings.py

# Celery Configuration


