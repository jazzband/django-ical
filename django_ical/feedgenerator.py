#:coding=utf-8:

from icalendar import Calendar, Event

from django.utils.feedgenerator import SyndicationFeed

__all__ = (
    'ICal20Feed',
)

FEED_FIELD_MAP = (
    ('product_id',          'prodid'),
    ('method',              'method'),
    ('title',               'x-wr-calname'),
    ('description',         'x-wr-caldesc'),
    ('timezone',            'x-wr-timezone'),
)

ITEM_EVENT_FIELD_MAP = (
    # item_guid は unique_id になる
    ('unique_id',           'uid'),
    ('title',               'summary'),
    ('description',         'description'),
    ('start_datetime',      'dtstart'),
    ('end_datetime',        'dtend'),
    ('updated',             'last-modified'),
    ('created',             'created'),
    ('timestamp',           'dtstamp'),
    ('transparency',        'transp'),
    ('location',            'location'),
    ('link',                'url'),
)

class ICal20Feed(SyndicationFeed):
    mime_type='text/calendar; charset=utf8'

    def write(self, outfile, encoding):
        cal = Calendar()
        cal.add('version', '2.0')
        cal.add('calscale', 'GREGORIAN')

        for ifield, efield in FEED_FIELD_MAP:
            val = self.feed.get(ifield)
            if val is not None:
                cal.add(efield, val)

        self.write_items(cal)

        to_ical = getattr(cal, 'as_string', None)
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
                    event.add(efield, val)
            calendar.add_component(event)
