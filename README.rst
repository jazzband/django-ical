django-ical
===========

|pypi| |docs| |build| |jazzband|

django-ical is a simple library/framework for creating
`iCal <http://www.ietf.org/rfc/rfc2445.txt>`_
feeds based in Django's
`syndication feed framework <https://docs.djangoproject.com/en/1.4/ref/contrib/syndication/>`_.

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

http://django-ical.readthedocs.io/en/latest/

Requirements
------------

* `Django <http://www.djangoproject.com/>`_ >= 1.8
* `icalendar <http://pypi.python.org/pypi/icalendar/>`_ >= 4.0.3


.. |pypi| image:: https://img.shields.io/pypi/v/django-ical.svg
    :alt: PyPI
    :target: https://pypi.org/project/django-ical/

.. |docs| image:: https://readthedocs.org/projects/django-ical/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: http://django-ical.readthedocs.io/en/latest/?badge=latest

.. |build| image:: https://travis-ci.org/jazzband/django-ical.svg?branch=master
    :target: https://travis-ci.org/jazzband/django-ical

.. |jazzband| image:: https://jazzband.co/static/img/badge.svg
   :target: https://jazzband.co/
   :alt: Jazzband
