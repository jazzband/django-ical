"""
iCalendar feed generation library -- used for generating
iCalendar feeds.

Sample usage:

>>> from django_ical import feedgenerator
>>> from datetime import datetime
>>> feed = feedgenerator.ICal20Feed(
...     title="My Events",
...     link="http://www.example.com/events.ical",
...     description="A iCalendar feed of my events.",
...     language="en",
... )
>>> feed.add_item(
...     title="Hello",
...     link="http://www.example.com/test/",
...     description="Testing."
...     start_datetime=datetime(2012, 5, 6, 10, 00),
...     end_datetime=datetime(2012, 5, 6, 12, 00),
... )
>>> fp = open('test.ical', 'w')
>>> feed.write(fp, 'utf-8')
>>> fp.close()

For definitions of the iCalendar format see:
http://www.ietf.org/rfc/rfc2445.txt
"""

from icalendar import Calendar, Event

from django.utils.feedgenerator import SyndicationFeed

__all__ = ("ICal20Feed", "DefaultFeed")

FEED_FIELD_MAP = (
    ("product_id", "prodid"),
    ("method", "method"),
    ("title", "x-wr-calname"),
    ("description", "x-wr-caldesc"),
    ("timezone", "x-wr-timezone"),
    (
        "ttl",
        "x-published-ttl",
    ),  # See format here: http://www.rfc-editor.org/rfc/rfc2445.txt (sec 4.3.6)
)

ITEM_EVENT_FIELD_MAP = (
    # 'item_guid' becomes 'unique_id' when passed to the SyndicationFeed
    ("unique_id", "uid"),
    ("title", "summary"),
    ("description", "description"),
    ("start_datetime", "dtstart"),
    ("end_datetime", "dtend"),
    ("updateddate", "last-modified"),
    ("created", "created"),
    ("timestamp", "dtstamp"),
    ("transparency", "transp"),
    ("location", "location"),
    ("geolocation", "geo"),
    ("link", "url"),
    ("organizer", "organizer"),
    ("categories", "categories"),
    ("rrule", "rrule"),
    ("exrule", "exrule"),
    ("rdate", "rdate"),
    ("exdate", "exdate"),
    ("status", "status"),
    ("attendee", "attendee"),
    ("valarm", None),
)


class ICal20Feed(SyndicationFeed):
    """
    iCalendar 2.0 Feed implementation.
    """

    mime_type = "text/calendar; charset=utf8"

    def write(self, outfile, encoding):  # pylint: disable=unused-argument
        """
        Writes the feed to the specified file in the
        specified encoding.
        """
        cal = Calendar()
        cal.add("version", "2.0")
        cal.add("calscale", "GREGORIAN")

        for ifield, efield in FEED_FIELD_MAP:
            val = self.feed.get(ifield)
            if val is not None:
                cal.add(efield, val)

        self.write_items(cal)

        to_ical = getattr(cal, "as_string", None)
        if not to_ical:
            to_ical = cal.to_ical
        outfile.write(to_ical())

    def write_items(self, calendar):
        """
        Write all events to the calendar
        """
        for item in self.items:
            event = Event()
            for ifield, efield in ITEM_EVENT_FIELD_MAP:
                val = item.get(ifield)
                if val is not None:
                    if ifield == "attendee":
                        for list_item in val:
                            event.add(efield, list_item)
                    elif ifield == "valarm":
                        for list_item in val:
                            event.add_component(list_item)
                    else:
                        event.add(efield, val)
            calendar.add_component(event)


DefaultFeed = ICal20Feed
