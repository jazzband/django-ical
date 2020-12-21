django-ical
===========

|pypi| |docs| |build| |coverage| |jazzband|

django-ical is a simple library/framework for creating
`iCal <http://www.ietf.org/rfc/rfc2445.txt>`_
feeds based in Django's
`syndication feed framework <https://docs.djangoproject.com/en/3.0/ref/contrib/syndication/>`_.

This documentation is modeled after the documentation for the syndication feed
framework so you can think of it as a simple extension.

If you are familiar with the Django syndication feed framework you should be
able to be able to use django-ical fairly quickly. It works the same way as
the Django syndication framework but adds a few extension properties to
support iCalendar feeds.

django-ical uses the `icalendar <http://pypi.python.org/pypi/icalendar/>`_ library
under the hood to generate iCalendar feeds.

Documentation
-------------

Documentation is hosted on Read the Docs:

https://django-ical.readthedocs.io/en/latest/


.. |pypi| image:: https://img.shields.io/pypi/v/django-ical.svg
    :alt: PyPI
    :target: https://pypi.org/project/django-ical/

.. |docs| image:: https://readthedocs.org/projects/django-ical/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: http://django-ical.readthedocs.io/en/latest/?badge=latest

.. |build| image:: https://github.com/jazzband/django-ical/workflows/Test/badge.svg
   :target: https://github.com/jazzband/django-ical/actions
   :alt: GitHub Actions

.. |coverage| image:: https://codecov.io/gh/jazzband/django-ical/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/jazzband/django-ical
   :alt: Coverage

.. |jazzband| image:: https://jazzband.co/static/img/badge.svg
   :target: https://jazzband.co/
   :alt: Jazzband
