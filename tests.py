import os
import sys
import django


def main():
    """
    Standalone django model test with a 'memory-only-django-installation'.
    You can play with a django model without a complete django app installation.
    http://www.djangosnippets.org/snippets/1044/
    """
    os.environ["DJANGO_SETTINGS_MODULE"] = "django.conf.global_settings"
    from django.conf import global_settings

    global_settings.SECRET_KEY = 'snakeoil'
    global_settings.TIME_ZONE = 'UTC'

    global_settings.INSTALLED_APPS = (
        'django.contrib.contenttypes',
        'django_ical',
    )
    global_settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }

    global_settings.MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
    )

    if django.VERSION > (1, 7):
        django.setup()

    from django.test.utils import get_runner
    test_runner = get_runner(global_settings)

    test_runner = test_runner()
    failures = test_runner.run_tests(['django_ical'])
    sys.exit(failures)

if __name__ == '__main__':
    main()
