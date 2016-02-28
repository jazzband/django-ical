#:coding=utf-8:

"""
Views for generating ical feeds.
"""

from datetime import datetime
from calendar import timegm

import django
from django.http import HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.syndication.views import Feed
from django.utils.http import http_date
try:
    from django.utils import six
except ImportError:
    import six

from django_ical import feedgenerator

__all__ = (
    'ICalFeed',
)

# Extra fields added to the Feed object
# to support ical
FEED_EXTRA_FIELDS = (
    'method',
    'product_id',
    'timezone',
)

# Extra fields added to items (events) to
# support ical
ICAL_EXTRA_FIELDS = [
    'timestamp',        # dtstamp
    'created',          # created
    'start_datetime',   # dtstart
    'end_datetime',     # dtend
    'transparency',     # transp
    'location',         # location
    'geolocation',      # latitude;longitude
    'organizer',        # email, cn, and role
]

# For Django <1.7
if django.VERSION < (1, 7):
    ICAL_EXTRA_FIELDS.append('updateddate')


class ICalFeed(Feed):
    """
    iCalendar Feed

    Existing Django syndication feeds

    :title: X-WR-CALNAME
    :description: X-WR-CALDESC
    :item_guid: UID
    :item_title: SUMMARY
    :item_description: DESCRIPTION
    :item_link: URL
    :item_updateddate: LAST-MODIFIED

    Extension fields

    :method: METHOD
    :timezone: X-WR-TIMEZONE
    :item_class: CLASS
    :item_timestamp: DTSTAMP
    :item_created: CREATED
    :item_start_datetime: DTSTART
    :item_end_datetime: DTEND
    :item_transparency: TRANSP
    """
    feed_type = feedgenerator.DefaultFeed

    def __call__(self, request, *args, **kwargs):
        """
        Copied from django.contrib.syndication.views.Feed

        Supports file_name as a dynamic attr.
        """
        try:
            obj = self.get_object(request, *args, **kwargs)
        except ObjectDoesNotExist:
            raise Http404('Feed object does not exist.')
        feedgen = self.get_feed(obj, request)
        response = HttpResponse(content_type=feedgen.mime_type)
        if hasattr(self, 'item_pubdate') or hasattr(self, 'item_updateddate'):
            # if item_pubdate or item_updateddate is defined for the feed, set
            # header so as ConditionalGetMiddleware is able to send 304 NOT MODIFIED
            response['Last-Modified'] = http_date(
                timegm(feedgen.latest_post_date().utctimetuple()))
        feedgen.write(response, 'utf-8')

        filename = self._get_dynamic_attr('file_name', obj)
        if filename:
            response['Content-Disposition'] = 'attachment; filename="%s"' % filename

        return response

    def _get_dynamic_attr(self, attname, obj, default=None):
        """
        Copied from django.contrib.syndication.views.Feed (v1.7.1)
        """
        try:
            attr = getattr(self, attname)
        except AttributeError:
            return default
        if callable(attr):
            # Check co_argcount rather than try/excepting the function and
            # catching the TypeError, because something inside the function
            # may raise the TypeError. This technique is more accurate.
            try:
                code = six.get_function_code(attr)
            except AttributeError:
                code = six.get_function_code(attr.__call__)
            if code.co_argcount == 2:       # one argument is 'self'
                return attr(obj)
            else:
                return attr()
        return attr

    # NOTE: Not used by icalendar but required
    #       by the Django syndication framework.
    link = ''

    def method(self, obj):
        return 'PUBLISH'

    def feed_extra_kwargs(self, obj):
        kwargs = {}
        for field in FEED_EXTRA_FIELDS:
            val = self._get_dynamic_attr(field, obj)
            if val:
                kwargs[field] = val
        return kwargs

    def item_timestamp(self, obj):
        return datetime.now()

    def item_extra_kwargs(self, obj):
        kwargs = {}
        for field in ICAL_EXTRA_FIELDS:
            val = self._get_dynamic_attr('item_' + field, obj)
            if val:
                kwargs[field] = val
        return kwargs
