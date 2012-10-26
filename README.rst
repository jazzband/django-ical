====================
django-ical
====================

django-ical is a simple library/framework for creating `ical
<http://www.ietf.org/rfc/rfc2445.txt>`_ feeds based in Django's `syndication
feed framework
<https://docs.djangoproject.com/en/1.4/ref/contrib/syndication/>`_. This
documentation is modeled after the documentation for the syndication feed
framework so you can think of it as a simple extension.

If you are familiar with the Django syndication feed framework you should be
able to be able to use django-ical fairly quickly. It works the same way as
the Django syndication framework but adds a few extension properties to
support iCalendar feeds.

django-ical uses the `icalendar <http://pypi.python.org/pypi/icalendar/>`_ library
under the hood to generate iCalendar feeds.

Docs
==============

Docs are hosted on Read the Docs: 
http://django-ics.readthedocs.org/en/latest/

Requirements
===================

* `Django <http://www.djangoproject.com/>`_ >= 1.2
* `icalendar <http://pypi.python.org/pypi/icalendar/>`_ >= 2.0.1
