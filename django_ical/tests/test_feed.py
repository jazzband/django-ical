from datetime import date
from datetime import datetime

from django.test import TestCase
from django.test.client import RequestFactory

import icalendar
import pytz

from django_ical import utils
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
            'recurrences': {
                'rrules': [utils.build_rrule(freq='DAILY', byhour=10),
                           utils.build_rrule(freq='MONTHLY', bymonthday=4)],
                'xrules': [utils.build_rrule(freq='MONTHLY', bymonthday=-4),
                           utils.build_rrule(freq='MONTHLY', byday='+3TU')],
                'rdates': [date(1999, 9, 2), date(1998, 1, 1)],
                'xdates': [date(1999, 8, 1), date(1998, 2, 1)],
            },
            'geolocation': (37.386013, -122.082932),
            'organizer': 'john.doe@example.com',
            'participants': [
                {
                    'name': 'Joe Unresponsive',
                    'email': 'joe.unresponsive@example.com',
                    'participation_status': 'NEEDS-ACTION'
                },
                {
                    'name': 'Jane Attender',
                    'email': 'jane.attender@example.com',
                    'participation_status': 'ACCEPTED'
                },
                {
                    'name': 'Dan Decliner',
                    'email': 'dan.decliner@example.com',
                    'participation_status': 'DECLINED'
                },
                {
                    'name': 'Mary Maybe',
                    'email': 'mary.maybe@example.com',
                    'participation_status': 'TENTATIVE'
                },
            ],
            'modified': datetime(2012, 5, 2, 10, 0),
        }, {
            'title': 'Title2',
            'description': 'Description2',
            'link': '/event/2',
            'start': datetime(2012, 5, 6, 18, 0),
            'end': datetime(2012, 5, 6, 20, 0),
            'recurrences': {
                'rrules': [utils.build_rrule(freq='WEEKLY', byday=['MO', 'TU', 'WE', 'TH', 'FR'])],
                'xrules': [utils.build_rrule(freq='MONTHLY', byday='-3TU')],
                'rdates': [date(1997, 9, 2)],
                'xdates': [date(1997, 8, 1)],
            },
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

    def item_rrule(self, obj):
        return obj['recurrences']['rrules']

    def item_exrule(self, obj):
        return obj['recurrences']['xrules']

    def item_rdate(self, obj):
        return obj['recurrences']['rdates']

    def item_exdate(self, obj):
        return obj['recurrences']['xdates']

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

    def item_attendee(self, obj):
        # All calendars support ATTENDEE attribute, however, for SUBSCRIBED calendars
        #   it appears that Apple calendar (desktop & iOS) displays event attendees, while Google & Outlook do not
        attendee_list = list()
        for participant in obj.participants:
            attendee = icalendar.vCalAddress('MAILTO:%s' % participant.email)
            attendee.params = {
                'cn': icalendar.vText(participant.name),
                'cutype': icalendar.vText('INDIVIDUAL'),
                'role': icalendar.vText('REQ-PARTICIPANT'),
                'rsvp': icalendar.vText('TRUE'),  # Does not seem to work for subscribed calendars.
                'partstat': icalendar.vText(participant.participation_status),
            }
            attendee_list.append(attendee)
        return attendee_list
    

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
        self.assertEquals(calendar.subcomponents[0]['DTSTART'].to_ical(), b'20120501T180000')
        self.assertEquals(calendar.subcomponents[0]['DTEND'].to_ical(), b'20120501T200000')
        self.assertEquals(calendar.subcomponents[0]['GEO'].to_ical(), "37.386013;-122.082932")
        self.assertEquals(calendar.subcomponents[0]['LAST-MODIFIED'].to_ical(), b'20120502T100000Z')
        self.assertEquals(calendar.subcomponents[0]['ORGANIZER'].to_ical(), b'MAILTO:john.doe@example.com')
        self.assertEquals(calendar.subcomponents[0]['ATTENDEE'][0].to_ical(),
                          b'ATTENDEE;CN="Joe Unresponsive";CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;RSVP=TRUE;PARTSTAT'
                          b'=NEEDS-ACTION:MAILTO:joe.unresponsive@example.com')
        self.assertEquals(calendar.subcomponents[0]['ATTENDEE'][1].to_ical(),
                          b'ATTENDEE;CN="Jane Attender";CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;RSVP=TRUE;PARTSTAT'
                          b'=ACCEPTED:MAILTO:jane.attender@example.com')
        self.assertEquals(calendar.subcomponents[0]['ATTENDEE'][2].to_ical(),
                          b'ATTENDEE;CN="Dan Decliner";CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;RSVP=TRUE;PARTSTAT'
                          b'=DECLINED:MAILTO:dan.decliner@example.com')
        self.assertEquals(calendar.subcomponents[0]['ATTENDEE'][2].to_ical(),
                          b'ATTENDEE;CN="Mary Maybe";CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;RSVP=TRUE;PARTSTAT'
                          b'=TENTATIVE:MAILTO:mary.maybe@example.com')
        self.assertEquals(calendar.subcomponents[0]['RRULE'][0].to_ical(), b'FREQ=DAILY;BYHOUR=10')
        self.assertEquals(calendar.subcomponents[0]['RRULE'][1].to_ical(), b'FREQ=MONTHLY;BYMONTHDAY=4')
        self.assertEquals(calendar.subcomponents[0]['EXRULE'][0].to_ical(), b'FREQ=MONTHLY;BYMONTHDAY=-4')
        self.assertEquals(calendar.subcomponents[0]['EXRULE'][1].to_ical(), b'FREQ=MONTHLY;BYDAY=+3TU')
        self.assertEquals(calendar.subcomponents[0]['RDATE'].to_ical(), b'19990902,19980101')
        self.assertEquals(calendar.subcomponents[0]['EXDATE'].to_ical(), b'19990801,19980201')

        self.assertEquals(calendar.subcomponents[1]['SUMMARY'], 'Title2')
        self.assertEquals(calendar.subcomponents[1]['DESCRIPTION'], 'Description2')
        self.assertTrue(calendar.subcomponents[1]['URL'].endswith('/event/2'))
        self.assertEquals(calendar.subcomponents[1]['DTSTART'].to_ical(), b'20120506T180000')
        self.assertEquals(calendar.subcomponents[1]['DTEND'].to_ical(), b'20120506T200000')
        self.assertEquals(calendar.subcomponents[1]['RRULE'].to_ical(), b'FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR')
        self.assertEquals(calendar.subcomponents[1]['EXRULE'].to_ical(), b'FREQ=MONTHLY;BYDAY=-3TU')
        self.assertEquals(calendar.subcomponents[1]['RDATE'].to_ical(), b'19970902')
        self.assertEquals(calendar.subcomponents[1]['EXDATE'].to_ical(), b'19970801')
        self.assertEquals(calendar.subcomponents[1]['GEO'].to_ical(), "37.386013;-122.082932")
        self.assertEquals(calendar.subcomponents[1]['LAST-MODIFIED'].to_ical(), b'20120507T100000Z')
        self.assertEquals(calendar.subcomponents[1]['ORGANIZER'].to_ical(), b'MAILTO:john.doe@example.com')

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
                    'recurrences': {
                        'rrules': [],
                        'xrules': [],
                        'rdates': [],
                        'xdates': [],
                    },
                }, {
                    'title': 'Title2',
                    'description': 'Description2',
                    'link': '/event/2',
                    'start': datetime(2012, 5, 6, 18, 00, tzinfo=us_eastern),
                    'end': datetime(2012, 5, 6, 20, 00, tzinfo=us_eastern),
                    'recurrences': {
                        'rrules': [],
                        'xrules': [],
                        'rdates': [],
                        'xdates': [],
                    },
                }]

        request = RequestFactory().get("/test/ical")
        view = TestTimezoneFeed()

        response = view(request)
        calendar = icalendar.Calendar.from_ical(response.content)
        self.assertEquals(len(calendar.subcomponents), 2)

        self.assertEquals(calendar.subcomponents[0]['DTSTART'].to_ical(), b'20120501T180000')
        self.assertEquals(calendar.subcomponents[0]['DTSTART'].params['TZID'], 'Asia/Tokyo')

        self.assertEquals(calendar.subcomponents[0]['DTEND'].to_ical(), b'20120501T200000')
        self.assertEquals(calendar.subcomponents[0]['DTEND'].params['TZID'], 'Asia/Tokyo')

        self.assertEquals(calendar.subcomponents[1]['DTSTART'].to_ical(), b'20120506T180000')
        self.assertEquals(calendar.subcomponents[1]['DTSTART'].params['TZID'], 'US/Eastern')

        self.assertEquals(calendar.subcomponents[1]['DTEND'].to_ical(), b'20120506T200000')
        self.assertEquals(calendar.subcomponents[1]['DTEND'].params['TZID'], 'US/Eastern')

    def test_file_name(self):
        request = RequestFactory().get("/test/ical")
        view = TestFilenameFeed()

        response = view(request)

        self.assertIn('Content-Disposition', response)
        self.assertEqual(response['content-disposition'], 'attachment; filename="123.ics"')
