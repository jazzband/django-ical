#:coding=utf-8:

import pytz
import icalendar
from datetime import datetime

from django.test import TestCase
from django.test.client import RequestFactory
from six import b

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
            'start': datetime(2012, 5, 1, 18, 0),
            'end': datetime(2012, 5, 1, 20, 0),
            'geolocation': (37.386013, -122.082932),
            'organizer': 'john.doe@example.com',
            'modified': datetime(2012, 5, 2, 10, 0),
        }, {
            'title': 'Title2',
            'description': 'Description2',
            'link': '/event/2',
            'start': datetime(2012, 5, 6, 18, 0),
            'end': datetime(2012, 5, 6, 20, 0),
            'geolocation': (37.386013, -122.082932),
            'modified': datetime(2012, 5, 7, 10, 0),
            'organizer': {
                'cn': 'John Doe',
                'email': 'john.doe@example.com',
                'role': 'CHAIR'
            },
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

    def item_geolocation(self, obj):
        return obj.get('geolocation', None)

    def item_updateddate(self, obj):
        return obj.get('modified', None)

    def item_pubdate(self, obj):
        return obj.get('modified', None)

    def item_organizer(self, obj):
        organizer_dic = obj.get('organizer', None)
        if organizer_dic:
            if isinstance(organizer_dic, dict):
                organizer = icalendar.vCalAddress('MAILTO:%s' % organizer_dic['email'])
                for key, val in organizer_dic.items():
                    if key is not 'email':
                        organizer.params[key] = icalendar.vText(val)
            else:
                organizer = icalendar.vCalAddress('MAILTO:%s' % organizer_dic)
            return organizer


class TestFilenameFeed(ICalFeed):
    feed_type = ICal20Feed
    title = "Test Filename Feed"
    description = "Test ICal Feed"

    def get_object(self, request):
        return {
            'id': 123,
        }

    def items(self, obj):
        return [obj]

    def file_name(self, obj):
        return "%s.ics" % obj['id']

    def item_link(self, item):
        return ''  # Required by the syndication framework


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
        self.assertEquals(calendar.subcomponents[0]['DTSTART'].to_ical(), b('20120501T180000'))
        self.assertEquals(calendar.subcomponents[0]['DTEND'].to_ical(), b('20120501T200000'))
        self.assertEquals(calendar.subcomponents[0]['GEO'].to_ical(), "37.386013;-122.082932")
        self.assertEquals(calendar.subcomponents[0]['LAST-MODIFIED'].to_ical(), b('20120502T100000Z'))
        self.assertEquals(calendar.subcomponents[0]['ORGANIZER'].to_ical(),
                          b("MAILTO:john.doe@example.com"))

        self.assertEquals(calendar.subcomponents[1]['SUMMARY'], 'Title2')
        self.assertEquals(calendar.subcomponents[1]['DESCRIPTION'], 'Description2')
        self.assertTrue(calendar.subcomponents[1]['URL'].endswith('/event/2'))
        self.assertEquals(calendar.subcomponents[1]['DTSTART'].to_ical(), b('20120506T180000'))
        self.assertEquals(calendar.subcomponents[1]['DTEND'].to_ical(), b('20120506T200000'))
        self.assertEquals(calendar.subcomponents[1]['GEO'].to_ical(), "37.386013;-122.082932")
        self.assertEquals(calendar.subcomponents[1]['LAST-MODIFIED'].to_ical(), b('20120507T100000Z'))
        self.assertEquals(calendar.subcomponents[1]['ORGANIZER'].to_ical(),
                          b("MAILTO:john.doe@example.com"))

    def test_wr_timezone(self):
        """
        Test for the x-wr-timezone property.
        """
        class TestTimezoneFeed(TestICalFeed):
            timezone = "Asia/Tokyo"

        request = RequestFactory().get("/test/ical")
        view = TestTimezoneFeed()

        response = view(request)
        calendar = icalendar.Calendar.from_ical(response.content)
        self.assertEquals(calendar['X-WR-TIMEZONE'], "Asia/Tokyo")

    def test_timezone(self):
        tokyo = pytz.timezone('Asia/Tokyo')
        us_eastern = pytz.timezone('US/Eastern')

        class TestTimezoneFeed(TestItemsFeed):
            def items(self):
                return [{
                    'title': 'Title1',
                    'description': 'Description1',
                    'link': '/event/1',
                    'start': datetime(2012, 5, 1, 18, 00, tzinfo=tokyo),
                    'end': datetime(2012, 5, 1, 20, 00, tzinfo=tokyo),

                }, {
                    'title': 'Title2',
                    'description': 'Description2',
                    'link': '/event/2',
                    'start': datetime(2012, 5, 6, 18, 00, tzinfo=us_eastern),
                    'end': datetime(2012, 5, 6, 20, 00, tzinfo=us_eastern),
                }]

        request = RequestFactory().get("/test/ical")
        view = TestTimezoneFeed()

        response = view(request)
        calendar = icalendar.Calendar.from_ical(response.content)
        self.assertEquals(len(calendar.subcomponents), 2)

        self.assertEquals(calendar.subcomponents[0]['DTSTART'].to_ical(), b('20120501T180000'))
        self.assertEquals(calendar.subcomponents[0]['DTSTART'].params['TZID'], 'Asia/Tokyo')

        self.assertEquals(calendar.subcomponents[0]['DTEND'].to_ical(), b('20120501T200000'))
        self.assertEquals(calendar.subcomponents[0]['DTEND'].params['TZID'], 'Asia/Tokyo')

        self.assertEquals(calendar.subcomponents[1]['DTSTART'].to_ical(), b('20120506T180000'))
        self.assertEquals(calendar.subcomponents[1]['DTSTART'].params['TZID'], 'US/Eastern')

        self.assertEquals(calendar.subcomponents[1]['DTEND'].to_ical(), b('20120506T200000'))
        self.assertEquals(calendar.subcomponents[1]['DTEND'].params['TZID'], 'US/Eastern')

    def test_file_name(self):
        request = RequestFactory().get("/test/ical")
        view = TestFilenameFeed()

        response = view(request)

        self.assertIn('Content-Disposition', response)
        self.assertEqual(response['content-disposition'], 'attachment; filename="123.ics"')
