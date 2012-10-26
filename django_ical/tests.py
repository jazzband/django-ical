#:coding=utf-8:

import icalendar
from datetime import datetime

import django
from django.test import TestCase

from django_ical.feedgenerator import ICal20Feed
from django_ical.views import ICalFeed

def request_factory(method, path, data={}, **extra):
    if django.VERSION >= (1,3):
        from django.test.client import RequestFactory

        return getattr(RequestFactory(), method)(
            path=path,
            data=data,
            **extra
        )
    else:
        import urlparse
        import urllib
        from django.http import SimpleCookie
        from django.utils.http import urlencode
        from django.core.handlers.wsgi import WSGIRequest
        from django.test.client import FakePayload
        try:
            from cStringIO import StringIO
        except ImportError:
            from StringIO import StringIO

        # This is a minimal valid WSGI environ dictionary, plus:
        # - HTTP_COOKIE: for cookie support,
        # - REMOTE_ADDR: often useful, see #8551.
        # See http://www.python.org/dev/peps/pep-3333/#environ-variables
        environ = {
            'HTTP_COOKIE':       SimpleCookie().output(header='', sep='; '),
            'PATH_INFO':         '/',
            'REMOTE_ADDR':       '127.0.0.1',
            'REQUEST_METHOD':    'GET',
            'SCRIPT_NAME':       '',
            'SERVER_NAME':       'testserver',
            'SERVER_PORT':       '80',
            'SERVER_PROTOCOL':   'HTTP/1.1',
            'wsgi.version':      (1,0),
            'wsgi.url_scheme':   'http',
            'wsgi.input':        FakePayload(''),
            'wsgi.errors':       StringIO(),
            'wsgi.multiprocess': True,
            'wsgi.multithread':  False,
            'wsgi.run_once':     False,
        }

        parsed = urlparse.urlparse(path)
        # If there are parameters, add them
        if parsed[3]:
            path = urllib.unquote(parsed[2] + ";" + parsed[3])
        else:
            path = urllib.unquote(parsed[2])

        r = {
            'CONTENT_TYPE':    'text/html; charset=utf-8',
            'PATH_INFO':       path,
            'QUERY_STRING':    urlencode(data, doseq=True) or parsed[4],
            'REQUEST_METHOD':  method.upper(),
        }
        environ.update(r)
        environ.update(extra)

        return WSGIRequest(environ)

class TestICalFeed(ICalFeed):
    feed_type = ICal20Feed
    title = "Test Feed"
    description = "Test ICal Feed"
    items = []

class TestItemsFeed(ICalFeed):
    feed_type = ICal20Feed
    title = "Test Feed"
    description = "Test ICal Feed"
    def items(self):
        return [{
            'title': 'Title1',
            'description': 'Description1',
            'link': '/event/1',
            'start': datetime(2012, 5, 1, 18, 00),
            'end': datetime(2012, 5, 1, 20, 00),

        }, {
            'title': 'Title2',
            'description': 'Description2',
            'link': '/event/2',
            'start': datetime(2012, 5, 6, 18, 00),
            'end': datetime(2012, 5, 6, 20, 00),
        }]

    def item_title(self, obj):
        return obj['title']
    def item_description(self, obj):
        return obj['description']
    def item_start_datetime(self, obj):
        return obj['start']
    def item_end_datetime(self, obj):
        return obj['end']
    def item_link(self, obj):
        return obj['link']

class ICal20FeedTest(TestCase):
    def test_basic(self):
        request = request_factory('get', "/test/ical")
        view = TestICalFeed()
        
        response = view(request)
        calendar = icalendar.Calendar.from_ical(response.content)
        self.assertEquals(calendar['X-WR-CALNAME'], "Test Feed")
        self.assertEquals(calendar['X-WR-CALDESC'], "Test ICal Feed")

    def test_items(self):
        request = request_factory('get', "/test/ical")
        view = TestItemsFeed()
        
        response = view(request)
        calendar = icalendar.Calendar.from_ical(response.content)
        self.assertEquals(len(calendar.subcomponents), 2)

        self.assertEquals(calendar.subcomponents[0]['SUMMARY'], 'Title1')
        self.assertEquals(calendar.subcomponents[0]['DESCRIPTION'], 'Description1')
        self.assertTrue(calendar.subcomponents[0]['URL'].endswith('/event/1'))
        self.assertEquals(calendar.subcomponents[0]['DTSTART'].to_ical(), '20120501T180000')
        self.assertEquals(calendar.subcomponents[0]['DTEND'].to_ical(), '20120501T200000')

        self.assertEquals(calendar.subcomponents[1]['SUMMARY'], 'Title2')
        self.assertEquals(calendar.subcomponents[1]['DESCRIPTION'], 'Description2')
        self.assertTrue(calendar.subcomponents[1]['URL'].endswith('/event/2'))
        self.assertEquals(calendar.subcomponents[1]['DTSTART'].to_ical(), '20120506T180000')
        self.assertEquals(calendar.subcomponents[1]['DTEND'].to_ical(), '20120506T200000')
