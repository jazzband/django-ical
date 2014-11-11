The high-level framework
========================

Overview
------------------------

The high level ical feed-generating is supplied by the :class:`ICalFeed
<django_ical.views.ICalFeed>` class.  To create a feed, write a
:class:`ICalFeed <django_ical.views.ICalFeed>` class and point to an instance
of it in your `URLconf <https://docs.djangoproject.com/en/1.4/topics/http/urls/>`_.

With RSS feeds, the items in the feed represent articles or simple web pages.
The :class:`ICalFeed <django_ical.views.ICalFeed>` class represents an
iCalendar calendar. Calendars contain items which are events.

Let's look at a simple example. Here the item_start_datetime is a django-ical
extension that supplies the start time of the event.

.. code-block:: python

    from django_ical.views import ICalFeed
    from examplecom.models import Event

    class EventFeed(ICalFeed):
        """
        A simple event calender
        """
        product_id = '-//example.com//Example//EN'
        timezone = 'UTC'

        def items(self):
            return Event.objects.all().order_by('-start_datetime')

        def item_title(self, item):
            return item.title

        def item_description(self, item):
            return item.description
        
        def item_start_datetime(self, item):
            return item.start_datetime

To connect a URL to this calendar, put an instance of the EventFeed object in
your URLconf. For example:

.. code-block:: python

    from django.conf.urls import patterns, url, include
    from myproject.feeds import EventFeed

    urlpatterns = patterns('',
        # ...
        (r'^latest/feed/$', EventFeed()),
        # ...
    )


Property Reference and Extensions
--------------------------------------

django-ical adds a number of extensions to the base syndication framework in
order to support iCalendar feeds and ignores many fields used in RSS feeds.
Here is a table of all of the fields that django-ical supports.

+-----------------------+-----------------------+-----------------------------+
| Property name         | iCalendar field name  | Description                 |
+=======================+=======================+=============================+
| product_id            | `PRODID`_             | The calendar product ID     |
+-----------------------+-----------------------+-----------------------------+
| timezone              | `X-WR-TIMEZONE`_      | The calendar timezone       |
+-----------------------+-----------------------+-----------------------------+
| title                 | `X-WR-CALNAME`_       | The calendar name/title     |
+-----------------------+-----------------------+-----------------------------+
| description           | `X-WR-CALDESC`_       | The calendar name/title     |
+-----------------------+-----------------------+-----------------------------+
| method                | `METHOD`_             | The calendar method such as |
|                       |                       | meeting requests.           |
+-----------------------+-----------------------+-----------------------------+
| item_guid             | `UID`_                | The event's unique id.      |
|                       |                       | This id should be           |
|                       |                       | *globally* unique so you    |
|                       |                       | should add an               | 
|                       |                       | @<domain_name> to your id.  |
+-----------------------+-----------------------+-----------------------------+
| item_title            | `SUMMARY`_            | The event name/title        |
+-----------------------+-----------------------+-----------------------------+
| item_description      | `DESCRIPTION`_        | The event description       |
+-----------------------+-----------------------+-----------------------------+
| item_link             | `URL`_                | The event url               |
+-----------------------+-----------------------+-----------------------------+
| item_class            | `CLASS`_              | The event class             |
|                       |                       | (e.g. PUBLIC, PRIVATE,      |
|                       |                       | CONFIDENTIAL)               |
+-----------------------+-----------------------+-----------------------------+
| item_created          | `CREATED`_            | The event create time       |
+-----------------------+-----------------------+-----------------------------+
| item_updated          | `LAST-MODIFIED`_      | The event modified time     |
+-----------------------+-----------------------+-----------------------------+
| item_start_datetime   | `DTSTART`_            | The event start time        |
+-----------------------+-----------------------+-----------------------------+
| item_end_datetime     | `DTEND`_              | The event end time          |
+-----------------------+-----------------------+-----------------------------+
| item_location         | `LOCATION`_           | The event lociation         |
+-----------------------+-----------------------+-----------------------------+
| item_geolocation      | `GEO`_                | The latitude and longitude  |
|                       |                       | of the event. The value     |
|                       |                       | returned by this property   |
|                       |                       | should be a two-tuple       |
|                       |                       | containing the latitude and |
|                       |                       | longitude as float values.  |
|                       |                       | semicolon. Ex:              |
|                       |                       | *(37.386013, -122.082932)*  |
+-----------------------+-----------------------+-----------------------------+
| item_transparency     | `TRANSP`_             | The event transparency.     |
|                       |                       | Defines whether the event   |
|                       |                       | shows up in busy searches.  |
|                       |                       | (e.g. OPAQUE, TRANSPARENT)  |
+-----------------------+-----------------------+-----------------------------+
| item_organizer        | `ORGANIZER`_          | The event organizer.        |
|                       |                       | Expected to be a            |
|                       |                       | vCalAddress object. See     |
|                       |                       | `iCalendar`_ documentation  |
|                       |                       | or tests to know how to     |
|                       |                       | build them.                 |
+-----------------------+-----------------------+-----------------------------+

Note:

* django-ical does not use the ``link`` property required by the Django
  syndication framework.

The low-level framework
========================

Behind the scenes, the high-level iCalendar framework uses a lower-level
framework for generating feeds' ical data. This framework lives in a single
module: :mod:`django_ical.feedgenerator`.

You use this framework on your own, for lower-level feed generation. You can
also create custom feed generator subclasses for use with the feed_type
option.

See: `The syndication feed framework: Specifying the type of feed <https://docs.djangoproject.com/en/1.4/ref/contrib/syndication/#specifying-the-type-of-feed>`_

.. _PRODID: http://www.kanzaki.com/docs/ical/prodid.html
.. _METHOD: http://www.kanzaki.com/docs/ical/method.html
.. _SUMMARY: http://www.kanzaki.com/docs/ical/summary.html
.. _DESCRIPTION: http://www.kanzaki.com/docs/ical/description.html
.. _UID: http://www.kanzaki.com/docs/ical/uid.html
.. _CLASS: http://www.kanzaki.com/docs/ical/class.html
.. _CREATED: http://www.kanzaki.com/docs/ical/created.html
.. _LAST-MODIFIED: http://www.kanzaki.com/docs/ical/lastModified.html
.. _DTSTART: http://www.kanzaki.com/docs/ical/dtstart.html
.. _DTEND: http://www.kanzaki.com/docs/ical/dtend.html
.. _GEO: http://www.kanzaki.com/docs/ical/geo.html
.. _LOCATION: http://www.kanzaki.com/docs/ical/location.html
.. _TRANSP: http://www.kanzaki.com/docs/ical/transp.html
.. _URL: http://www.kanzaki.com/docs/ical/url.html
.. _ORGANIZER: http://www.kanzaki.com/docs/ical/organizer.html
.. _X-WR-CALNAME: http://en.wikipedia.org/wiki/ICalendar#Calendar_extensions
.. _X-WR-CALDESC: http://en.wikipedia.org/wiki/ICalendar#Calendar_extensions
.. _X-WR-TIMEZONE: http://en.wikipedia.org/wiki/ICalendar#Calendar_extensions
.. _iCalendar: http://icalendar.readthedocs.org/en/latest/index.html
