import os
import sys


def main():
    """
    Standalone Django model test with a 'memory-only-django-installation'.
    You can play with a django model without a complete django app installation.
    http://www.djangosnippets.org/snippets/1044/
    """

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_settings")
    print(os.environ)

    import django
    from django.conf import settings

    django.setup()

    from django.test.utils import get_runner

    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["django_ical"])
    sys.exit(bool(failures))


if __name__ == "__main__":
    main()
