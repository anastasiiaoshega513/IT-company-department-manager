from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}