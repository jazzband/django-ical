#:coding=utf-8:

import icalendar
from datetime import datetime

from django.test import TestCase
from django.test.client import RequestFactory

from django_ical.feedgenerator import ICal20Feed
from django_ical.views import ICalFeed

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
        request = RequestFactory().get("/test/ical")
        view = TestICalFeed()
        
        response = view(request)
        calendar = icalendar.Calendar.from_ical(response.content)
        self.assertEquals(calendar['X-WR-CALNAME'], "Test Feed")
        self.assertEquals(calendar['X-WR-CALDESC'], "Test ICal Feed")

    def test_items(self):
        request = RequestFactory().get("/test/ical")
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
