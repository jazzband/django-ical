TIME_ZONE="UTC"
SECRET_KEY="snakeoil"

DATABASES={
  "default": {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": ":memory:",
  }
}

INSTALLED_APPS=[
  "django.contrib.contenttypes",
  "django_ical",
]

MIDDLEWARE_CLASSES=[
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
]

