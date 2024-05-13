The high-level framework
========================

Overview
--------

The high level iCal feed-generating is supplied by the
:class:`ICalFeed <django_ical.views.ICalFeed>` class.
To create a feed, write a :class:`ICalFeed <django_ical.views.ICalFeed>`
class and point to an instance of it in your
`URLconf <https://docs.djangoproject.com/en/4.2/topics/http/urls/>`_.

With RSS feeds, the items in the feed represent articles or simple web pages.
The :class:`ICalFeed <django_ical.views.ICalFeed>` class represents an
iCalendar calendar. Calendars contain items which are events.

Example
-------

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
        file_name = "event.ics"

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

    urlpatterns = [
        # ...
        path('latest/feed.ics', EventFeed()),
        # ...
    ]

Example how recurrences are built using the django-recurrence_ package:

.. code-block:: python

    from django_ical.utils import build_rrule_from_recurrences_rrule
    from django_ical.views import ICalFeed
    from examplecom.models import Event

    class EventFeed(ICalFeed):
        """
        A simple event calender
        """
        # ...

        def item_rrule(self, item):
            """Adapt Event recurrence to Feed Entry rrule."""
            if item.recurrences:
                rules = []
                for rule in item.recurrences.rrules:
                    rules.append(build_rrule_from_recurrences_rrule(rule))
                return rules

        def item_exrule(self, item):
            """Adapt Event recurrence to Feed Entry exrule."""
            if item.recurrences:
                rules = []
                for rule in item.recurrences.exrules:
                    rules.append(build_rrule_from_recurrences_rrule(rule))
                return rules

        def item_rdate(self, item):
            """Adapt Event recurrence to Feed Entry rdate."""
            if item.recurrences:
                return item.recurrences.rdates

        def item_exdate(self, item):
            """Adapt Event recurrence to Feed Entry exdate."""
            if item.recurrences:
                return item.recurrences.exdates

Note that in ``django_ical.utils`` are also convienience methods to build ``rrules`` from
scratch, from string (serialized iCal) and ``dateutil.rrule``.


File Downloads
--------------

The `file_name` parameter is an optional used as base name when generating the file. By
default django-ical will not set the Content-Disposition header of the response. By setting
the file_name parameter you can cause django_ical to set the Content-Disposition header
and set the file name. In the example below, it will be called "event.ics".

.. code-block:: python

    class EventFeed(ICalFeed):
        """
        A simple event calender
        """
        product_id = '-//example.com//Example//EN'
        timezone = 'UTC'
        file_name = "event.ics"

        # ...

The `file_name` parameter can be a method like other properties. Here we can set
the file name to include the id of the object returned by `get_object()`.

.. code-block:: python

    class EventFeed(ICalFeed):
        """
        A simple event calender
        """
        product_id = '-//example.com//Example//EN'
        timezone = 'UTC'

        def file_name(self, obj):
            return "feed_%s.ics" % obj.id

        # ...


Alarms
------

Alarms must be `icalendar.Alarm` objects, a list is expected as the return value for
`item_valarm`.

.. code-block:: python

    from icalendar import Alarm
    from datetime import timedelta
    
    def item_valarm(self, item):
        valarm = Alarm()
        valarm.add('action', 'display')
        valarm.add('description', 'Your message text')
        valarm.add('trigger', timedelta(days=-1))
        return [valarm]


Tasks (Todos)
-------------

It is also possible to generate representations of tasks (or deadlines, todos)
which are represented in iCal with the dedicated `VTODO` component instead of the usual `VEVENT`.

To do so, you can use a specific method to determine which type of component a given item
should be translated as:

.. code-block:: python

    from django_ical.views import ICalFeed
    from examplecom.models import Deadline

    class EventFeed(ICalFeed):
        """
        A simple event calender with tasks
        """
        product_id = '-//example.com//Example//EN'
        timezone = 'UTC'
        file_name = "event.ics"

        def items(self):
            return Deadline.objects.all().order_by('-due_datetime')

        def item_component_type(self):
            return 'todo' # could also be 'event', which is the default

        def item_title(self, item):
            return item.title

        def item_description(self, item):
            return item.description

        def item_due_datetime(self, item):
            return item.due_datetime




Property Reference and Extensions
---------------------------------

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
| description           | `X-WR-CALDESC`_       | The calendar description    |
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
| item_updateddate      | `LAST-MODIFIED`_      | The event modified time     |
+-----------------------+-----------------------+-----------------------------+
| item_start_datetime   | `DTSTART`_            | The event start time        |
+-----------------------+-----------------------+-----------------------------+
| item_end_datetime     | `DTEND`_              | The event end time          |
+-----------------------+-----------------------+-----------------------------+
| item_location         | `LOCATION`_           | The event location          |
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
| item_attendee         | `ATTENDEE`_           | The event attendees.        |
|                       |                       | Expected to be a list of    |
|                       |                       | vCalAddress objects. See    |
|                       |                       | `iCalendar`_ documentation  |
|                       |                       | or tests to know how to     |
|                       |                       | build them.                 |
+-----------------------+-----------------------+-----------------------------+
| item_rrule            | `RRULE`_              | The recurrence rule for     |
|                       |                       | repeating events.           |
|                       |                       | See `iCalendar`_            |
|                       |                       | documentation or tests to   |
|                       |                       | know how to build them.     |
+-----------------------+-----------------------+-----------------------------+
| item_rdate            | `RDATE`_              | The recurring dates/times   |
|                       |                       | for a repeating event.      |
|                       |                       | See `iCalendar`_            |
|                       |                       | documentation or tests to   |
|                       |                       | know how to build them.     |
+-----------------------+-----------------------+-----------------------------+
| item_exdate           | `EXDATE`_             | The dates/times for         |
|                       |                       | exceptions of a recurring   |
|                       |                       | event.                      |
|                       |                       | See `iCalendar`_            |
|                       |                       | documentation or tests to   |
|                       |                       | know how to build them.     |
+-----------------------+-----------------------+-----------------------------+
| item_valarm           | `VALARM`_             | Alarms for the event, must  |
|                       |                       | be a list of Alarm objects. |
|                       |                       | See `iCalendar`_            |
|                       |                       | documentation or tests to   |
|                       |                       | know how to build them.     |
+-----------------------+-----------------------+-----------------------------+
| item_status           | `STATUS`_             | The status of an event.     |
|                       |                       | Can be CONFIRMED, CANCELLED |
|                       |                       | or TENTATIVE.               |
+-----------------------+-----------------------+-----------------------------+
| item_completed        | `COMPLETED`_          | The date a task was         |
|                       |                       | completed.                  |
+-----------------------+-----------------------+-----------------------------+
| item_percent_complete | `PERCENT-COMPLETE`_   | A number from 0 to 100      |
|                       |                       | indication the completion   |
|                       |                       | of the task.                |
+-----------------------+-----------------------+-----------------------------+
| item_priority         | `PRIORITY`_           | An integer from 0 to 9.     |
|                       |                       | 0 means undefined.          |
|                       |                       | 1 means highest priority.   |
+-----------------------+-----------------------+-----------------------------+
| item_due              | `DUE`_                | The date a task is due.     |
+-----------------------+-----------------------+-----------------------------+
| item_categories       | `CATEGORIES`_         | A list of strings, each     |
|                       |                       | being a category of the     |
|                       |                       | task.                       |
+-----------------------+-----------------------+-----------------------------+
| calscale              | `CALSCALE`_           | Not yet documented.         |
+-----------------------+-----------------------+-----------------------------+
| method                | `METHOD`_             | Not yet documented.         |
+-----------------------+-----------------------+-----------------------------+
| prodid                | `PRODID`_             | Not yet documented.         |
+-----------------------+-----------------------+-----------------------------+
| version               | `VERSION`_            | Not yet documented.         |
+-----------------------+-----------------------+-----------------------------+
| attach                | `ATTACH`_             | Not yet documented.         |
+-----------------------+-----------------------+-----------------------------+
| class                 | `CLASS`_              | Not yet documented.         |
+-----------------------+-----------------------+-----------------------------+
| comment               | `COMMENT`_            | Not yet documented.         |
+-----------------------+-----------------------+-----------------------------+
| resources             | `RESOURCES`_          | Not yet documented.         |
+-----------------------+-----------------------+-----------------------------+
| duration              | `DURATION`_           | Not yet documented.         |
+-----------------------+-----------------------+-----------------------------+
| freebusy              | `FREEBUSY`_           | Not yet documented.         |
+-----------------------+-----------------------+-----------------------------+
| tzid                  | `TZID`_               | Not yet documented.         |
+-----------------------+-----------------------+-----------------------------+
| tzname                | `TZNAME`_             | Not yet documented.         |
+-----------------------+-----------------------+-----------------------------+
| tzoffsetfrom          | `TZOFFSETFROM`_       | Not yet documented.         |
+-----------------------+-----------------------+-----------------------------+
| tzoffsetto            | `TZOFFSETTO`_         | Not yet documented.         |
+-----------------------+-----------------------+-----------------------------+
| tzurl                 | `TZURL`_              | Not yet documented.         |
+-----------------------+-----------------------+-----------------------------+
| contact               | `CONTACT`_            | Not yet documented.         |
+-----------------------+-----------------------+-----------------------------+
| recurrence_id         | `RECURRENCE_ID`_      | Not yet documented.         |
+-----------------------+-----------------------+-----------------------------+
| related_to            | `RELATED_TO`_         | Not yet documented.         |
+-----------------------+-----------------------+-----------------------------+
| action                | `ACTION`_             | Not yet documented.         |
+-----------------------+-----------------------+-----------------------------+
| repeat                | `REPEAT`_             | Not yet documented.         |
+-----------------------+-----------------------+-----------------------------+
| trigger               | `TRIGGER`_            | Not yet documented.         |
+-----------------------+-----------------------+-----------------------------+
| sequence              | `SEQUENCE`_           | Not yet documented.         |
+-----------------------+-----------------------+-----------------------------+
| request_status        | `REQUEST_STATUS`_     | Not yet documented.         |
+-----------------------+-----------------------+-----------------------------+


.. note::
   django-ical does not use the ``link`` property required by the Django
   syndication framework.

The low-level framework
========================

Behind the scenes, the high-level iCalendar framework uses a lower-level
framework for generating feeds' ical data. This framework lives in a single
module: :mod:`django_ical.feedgenerator`.

You use this framework on your own, for lower-level feed generation. You can
also create custom feed generator subclasses for use with the feed_type
option.

See: `The syndication feed framework: Specifying the type of feed <https://docs.djangoproject.com/en/1.9/ref/contrib/syndication/#specifying-the-type-of-feed>`_

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
.. _ATTENDEE: https://www.kanzaki.com/docs/ical/attendee.html
.. _RRULE: https://www.kanzaki.com/docs/ical/rrule.html
.. _EXRULE: https://www.kanzaki.com/docs/ical/exrule.html
.. _RDATE: https://www.kanzaki.com/docs/ical/rdate.html
.. _EXDATE: https://www.kanzaki.com/docs/ical/exdate.html
.. _STATUS: https://www.kanzaki.com/docs/ical/status.html
.. _VALARM: https://www.kanzaki.com/docs/ical/valarm.html
.. _COMPLETED: https://www.kanzaki.com/docs/ical/completed.html
.. _PERCENT-COMPLETE: https://www.kanzaki.com/docs/ical/percentComplete.html
.. _PRIORITY: https://www.kanzaki.com/docs/ical/priority.html
.. _DUE: https://www.kanzaki.com/docs/ical/due.html
.. _CALSCALE: https://www.kanzaki.com/docs/ical/calscale.html
.. _METHOD: https://www.kanzaki.com/docs/ical/method.html
.. _PRODID: https://www.kanzaki.com/docs/ical/prodid.html
.. _VERSION: https://www.kanzaki.com/docs/ical/version.html
.. _ATTACH: https://www.kanzaki.com/docs/ical/attach.html
.. _CLASS: https://www.kanzaki.com/docs/ical/class.html
.. _COMMENT: https://www.kanzaki.com/docs/ical/comment.html
.. _RESOURCES: https://www.kanzaki.com/docs/ical/resources.html
.. _DURATION: https://www.kanzaki.com/docs/ical/duration.html
.. _FREEBUSY: https://www.kanzaki.com/docs/ical/freebusy.html
.. _TZID: https://www.kanzaki.com/docs/ical/tzid.html
.. _TZNAME: https://www.kanzaki.com/docs/ical/tzname.html
.. _TZOFFSETFROM: https://www.kanzaki.com/docs/ical/tzoffsetfrom.html
.. _TZOFFSETTO: https://www.kanzaki.com/docs/ical/tzoffsetto.html
.. _TZURL: https://www.kanzaki.com/docs/ical/tzurl.html
.. _CONTACT: https://www.kanzaki.com/docs/ical/contact.html
.. _RECURRENCE-ID: https://www.kanzaki.com/docs/ical/recurrenceId.html
.. _RELATED-TO: https://www.kanzaki.com/docs/ical/relatedTo.html
.. _ACTION: https://www.kanzaki.com/docs/ical/action.html
.. _REPEAT: https://www.kanzaki.com/docs/ical/repeat.html
.. _TRIGGER: https://www.kanzaki.com/docs/ical/trigger.html
.. _SEQUENCE: https://www.kanzaki.com/docs/ical/sequence.html
.. _REQUEST-STATUS: https://icalendar.org/iCalendar-RFC-5545/3-8-8-3-request-status.html
.. _X-WR-CALNAME: http://en.wikipedia.org/wiki/ICalendar#Calendar_extensions
.. _X-WR-CALDESC: http://en.wikipedia.org/wiki/ICalendar#Calendar_extensions
.. _X-WR-TIMEZONE: http://en.wikipedia.org/wiki/ICalendar#Calendar_extensions
.. _iCalendar: http://icalendar.readthedocs.org/en/latest/index.html
.. _CATEGORIES: https://www.kanzaki.com/docs/ical/categories.html
.. _django-recurrence: https://github.com/django-recurrence/django-recurrence
