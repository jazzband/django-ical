.. django-ical documentation master file, created by
   sphinx-quickstart on Sun May  6 14:57:42 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


django-ical documentation
=========================

django-ical is a simple library/framework for creating
`ical <http://www.ietf.org/rfc/rfc2445.txt>`_
feeds based in Django's
`syndication feed framework <https://docs.djangoproject.com/en/1.9/ref/contrib/syndication/>`_.

This documentation is modeled after the documentation for the
syndication feed framework so you can think of it as a simple extension.

If you are familiar with the Django syndication feed framework you should be
able to be able to use django-ical fairly quickly. It works the same way as
the Django syndication framework but adds a few extension properties to
support iCalendar feeds.

django-ical uses the
`icalendar <http://pypi.python.org/pypi/icalendar/>`_
library under the hood to generate iCalendar feeds.


Contents
========

.. toctree::

   usage
   reference/index
   changelog


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

