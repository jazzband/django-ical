#:coding=utf-8:

import icalendar

from django.test import TestCase
from django.test.client import RequestFactory

from django_ical.feedgenerator import ICal20Feed
from django_ical.views import ICalFeed

class TestICalFeed(ICalFeed):
    feed_type = ICal20Feed
    title = "Test Feed"
    description = "Test ICal Feed"
    items = []

class ICal20FeedTest(TestCase):
    def test_basic(self):
        request = RequestFactory().get("/test/ical")
        view = TestICalFeed()
        
        response = view(request)
        calendar = icalendar.Calendar.from_ical(response.content)
        self.assertEquals(calendar['X-WR-CALNAME'], "Test Feed")
        self.assertEquals(calendar['X-WR-CALDESC'], "Test ICal Feed")
