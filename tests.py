import os
import sys


def main():
    """
    Standalone Django model test with a 'memory-only-django-installation'.
    You can play with a django model without a complete django app installation.
    http://www.djangosnippets.org/snippets/1044/
    """

    import django
    from django.conf import settings

    settings.configure(
        DATABASES={
            "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
        },
        INSTALLED_APPS=["django.contrib.contenttypes", "django_ical"],
        MIDDLEWARE_CLASSES=[
            "django.middleware.common.CommonMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
        ],
        SECRET_KEY="snakeoil",
        TIME_ZONE="UTC",
    )

    django.setup()

    from django.test.utils import get_runner

    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["django_ical"])
    sys.exit(bool(failures))


if __name__ == "__main__":
    main()
