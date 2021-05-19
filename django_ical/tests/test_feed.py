from datetime import date
from datetime import datetime
from datetime import timedelta
from os import linesep

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
        return [
            {
                "title": "Title1",
                "description": "Description1",
                "link": "/event/1",
                "start": datetime(2012, 5, 1, 18, 0),
                "end": datetime(2012, 5, 1, 20, 0),
                "recurrences": {
                    "rrules": [
                        utils.build_rrule(freq="DAILY", byhour=10),
                        utils.build_rrule(freq="MONTHLY", bymonthday=4),
                    ],
                    "xrules": [
                        utils.build_rrule(freq="MONTHLY", bymonthday=-4),
                        utils.build_rrule(freq="MONTHLY", byday="+3TU"),
                    ],
                    "rdates": [date(1999, 9, 2), date(1998, 1, 1)],
                    "xdates": [date(1999, 8, 1), date(1998, 2, 1)],
                },
                "geolocation": (37.386013, -122.082932),
                "organizer": "john.doe@example.com",
                "participants": [
                    {
                        "email": "joe.unresponsive@example.com",
                        "cn": "Joe Unresponsive",
                        "partstat": "NEEDS-ACTION",
                    },
                    {
                        "email": "jane.attender@example.com",
                        "cn": "Jane Attender",
                        "partstat": "ACCEPTED",
                    },
                    {
                        "email": "dan.decliner@example.com",
                        "cn": "Dan Decliner",
                        "partstat": "DECLINED",
                    },
                    {
                        "email": "mary.maybe@example.com",
                        "cn": "Mary Maybe",
                        "partstat": "TENTATIVE",
                    },
                ],
                "modified": datetime(2012, 5, 2, 10, 0),
            },
            {
                "title": "Title2",
                "description": "Description2",
                "link": "/event/2",
                "start": datetime(2012, 5, 6, 18, 0),
                "end": datetime(2012, 5, 6, 20, 0),
                "recurrences": {
                    "rrules": [
                        utils.build_rrule(
                            freq="WEEKLY", byday=["MO", "TU", "WE", "TH", "FR"]
                        )
                    ],
                    "xrules": [utils.build_rrule(freq="MONTHLY", byday="-3TU")],
                    "rdates": [date(1997, 9, 2)],
                    "xdates": [date(1997, 8, 1)],
                },
                "geolocation": (37.386013, -122.082932),
                "modified": datetime(2012, 5, 7, 10, 0),
                "organizer": {
                    "cn": "John Doe",
                    "email": "john.doe@example.com",
                    "role": "CHAIR",
                },
                "alarms": [
                    {
                        "trigger": timedelta(minutes=-30),
                        "action": "DISPLAY",
                        "description": "Alarm2a",
                    },
                    {
                        "trigger": timedelta(days=-1),
                        "action": "DISPLAY",
                        "description": "Alarm2b",
                    },
                ],
            },
        ]

    def item_title(self, obj):
        return obj["title"]

    def item_description(self, obj):
        return obj["description"]

    def item_start_datetime(self, obj):
        return obj["start"]

    def item_end_datetime(self, obj):
        return obj["end"]

    def item_rrule(self, obj):
        return obj["recurrences"]["rrules"]

    def item_exrule(self, obj):
        return obj["recurrences"]["xrules"]

    def item_rdate(self, obj):
        return obj["recurrences"]["rdates"]

    def item_exdate(self, obj):
        return obj["recurrences"]["xdates"]

    def item_link(self, obj):
        return obj["link"]

    def item_geolocation(self, obj):
        return obj.get("geolocation", None)

    def item_updateddate(self, obj):
        return obj.get("modified", None)

    def item_pubdate(self, obj):
        return obj.get("modified", None)

    def item_organizer(self, obj):
        organizer_dic = obj.get("organizer", None)
        if organizer_dic:
            if isinstance(organizer_dic, dict):
                organizer = icalendar.vCalAddress("MAILTO:%s" % organizer_dic["email"])
                for key, val in organizer_dic.items():
                    if key != "email":
                        organizer.params[key] = icalendar.vText(val)
            else:
                organizer = icalendar.vCalAddress("MAILTO:%s" % organizer_dic)
            return organizer

    def item_attendee(self, obj):
        """All calendars support ATTENDEE attribute, however, at this time, Apple calendar (desktop & iOS) and Outlook
        display event attendees, while Google does not. For SUBSCRIBED calendars it seems that it is not possible to
        use the default method to respond. As an alternative, you may review adding custom links to your description
        or setting up something like CalDav with authentication, which can enable the ability for attendees to respond
        via the default icalendar protocol."""
        participants = obj.get("participants", None)
        if participants:
            attendee_list = list()
            default_attendee_params = {
                "cutype": icalendar.vText("INDIVIDUAL"),
                "role": icalendar.vText("REQ-PARTICIPANT"),
                "rsvp": icalendar.vText(
                    "TRUE"
                ),  # Does not seem to work for subscribed calendars.
            }
            for participant in participants:
                attendee = icalendar.vCalAddress("MAILTO:%s" % participant.pop("email"))
                participant_dic = default_attendee_params.copy()
                participant_dic.update(participant)
                for key, val in participant_dic.items():
                    attendee.params[key] = icalendar.vText(val)
                attendee_list.append(attendee)
            return attendee_list

    def item_valarm(self, obj):
        alarms = obj.get("alarms", None)
        if alarms:
            alarm_list = list()
            for alarm in alarms:
                valarm = icalendar.Alarm()
                for key, value in alarm.items():
                    valarm.add(key, value)
                alarm_list.append(valarm)
            return alarm_list


class TestFilenameFeed(ICalFeed):
    feed_type = ICal20Feed
    title = "Test Filename Feed"
    description = "Test ICal Feed"

    def get_object(self, request):
        return {"id": 123}

    def items(self, obj):
        return [obj]

    def file_name(self, obj):
        return "%s.ics" % obj["id"]

    def item_link(self, item):
        return ""  # Required by the syndication framework


class ICal20FeedTest(TestCase):
    def test_basic(self):
        request = RequestFactory().get("/test/ical")
        view = TestICalFeed()

        response = view(request)
        calendar = icalendar.Calendar.from_ical(response.content)
        self.assertEqual(calendar["X-WR-CALNAME"], "Test Feed")
        self.assertEqual(calendar["X-WR-CALDESC"], "Test ICal Feed")

    def test_items(self):
        request = RequestFactory().get("/test/ical")
        view = TestItemsFeed()

        response = view(request)

        calendar = icalendar.Calendar.from_ical(response.content)
        self.assertEqual(len(calendar.subcomponents), 2)

        self.assertEqual(calendar.subcomponents[0]["SUMMARY"], "Title1")
        self.assertEqual(calendar.subcomponents[0]["DESCRIPTION"], "Description1")
        self.assertTrue(calendar.subcomponents[0]["URL"].endswith("/event/1"))
        self.assertEqual(
            calendar.subcomponents[0]["DTSTART"].to_ical(), b"20120501T180000"
        )
        self.assertEqual(
            calendar.subcomponents[0]["DTEND"].to_ical(), b"20120501T200000"
        )
        self.assertEqual(
            calendar.subcomponents[0]["GEO"].to_ical(), "37.386013;-122.082932"
        )
        self.assertEqual(
            calendar.subcomponents[0]["LAST-MODIFIED"].to_ical(), b"20120502T100000Z"
        )
        self.assertEqual(
            calendar.subcomponents[0]["ORGANIZER"].to_ical(),
            b"MAILTO:john.doe@example.com",
        )
        self.assertEqual(
            calendar.subcomponents[0]["ATTENDEE"][0].to_ical(),
            b"MAILTO:joe.unresponsive@example.com",
        )
        self.assertEqual(
            calendar.subcomponents[0]["ATTENDEE"][0].params.to_ical(),
            b'CN="Joe Unresponsive";CUTYPE=INDIVIDUAL;PARTSTAT=NEEDS-ACTION;ROLE=REQ-PARTICIPANT;'
            b"RSVP=TRUE",
        )
        self.assertEqual(
            calendar.subcomponents[0]["ATTENDEE"][1].to_ical(),
            b"MAILTO:jane.attender@example.com",
        )
        self.assertEqual(
            calendar.subcomponents[0]["ATTENDEE"][1].params.to_ical(),
            b'CN="Jane Attender";CUTYPE=INDIVIDUAL;PARTSTAT=ACCEPTED;ROLE=REQ-PARTICIPANT;RSVP=TRUE',
        )
        self.assertEqual(
            calendar.subcomponents[0]["ATTENDEE"][2].to_ical(),
            b"MAILTO:dan.decliner@example.com",
        )
        self.assertEqual(
            calendar.subcomponents[0]["ATTENDEE"][2].params.to_ical(),
            b'CN="Dan Decliner";CUTYPE=INDIVIDUAL;PARTSTAT=DECLINED;ROLE=REQ-PARTICIPANT;RSVP=TRUE',
        )
        self.assertEqual(
            calendar.subcomponents[0]["ATTENDEE"][3].to_ical(),
            b"MAILTO:mary.maybe@example.com",
        )
        self.assertEqual(
            calendar.subcomponents[0]["ATTENDEE"][3].params.to_ical(),
            b'CN="Mary Maybe";CUTYPE=INDIVIDUAL;PARTSTAT=TENTATIVE;ROLE=REQ-PARTICIPANT;RSVP=TRUE',
        )
        self.assertEqual(
            calendar.subcomponents[0]["RRULE"][0].to_ical(), b"FREQ=DAILY;BYHOUR=10"
        )
        self.assertEqual(
            calendar.subcomponents[0]["RRULE"][1].to_ical(),
            b"FREQ=MONTHLY;BYMONTHDAY=4",
        )
        self.assertEqual(
            calendar.subcomponents[0]["EXRULE"][0].to_ical(),
            b"FREQ=MONTHLY;BYMONTHDAY=-4",
        )
        self.assertEqual(
            calendar.subcomponents[0]["EXRULE"][1].to_ical(), b"FREQ=MONTHLY;BYDAY=+3TU"
        )
        self.assertEqual(
            calendar.subcomponents[0]["RDATE"].to_ical(), b"19990902,19980101"
        )
        self.assertEqual(
            calendar.subcomponents[0]["EXDATE"].to_ical(), b"19990801,19980201"
        )

        self.assertEqual(calendar.subcomponents[1]["SUMMARY"], "Title2")
        self.assertEqual(calendar.subcomponents[1]["DESCRIPTION"], "Description2")
        self.assertTrue(calendar.subcomponents[1]["URL"].endswith("/event/2"))
        self.assertEqual(
            calendar.subcomponents[1]["DTSTART"].to_ical(), b"20120506T180000"
        )
        self.assertEqual(
            calendar.subcomponents[1]["DTEND"].to_ical(), b"20120506T200000"
        )
        self.assertEqual(
            calendar.subcomponents[1]["RRULE"].to_ical(),
            b"FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR",
        )
        self.assertEqual(
            calendar.subcomponents[1]["EXRULE"].to_ical(), b"FREQ=MONTHLY;BYDAY=-3TU"
        )
        self.assertEqual(calendar.subcomponents[1]["RDATE"].to_ical(), b"19970902")
        self.assertEqual(calendar.subcomponents[1]["EXDATE"].to_ical(), b"19970801")
        self.assertEqual(
            calendar.subcomponents[1]["GEO"].to_ical(), "37.386013;-122.082932"
        )
        self.assertEqual(
            calendar.subcomponents[1]["LAST-MODIFIED"].to_ical(), b"20120507T100000Z"
        )
        self.assertEqual(
            calendar.subcomponents[1]["ORGANIZER"].to_ical(),
            b"MAILTO:john.doe@example.com",
        )
        self.assertIn(
            b"BEGIN:VALARM\r\nACTION:DISPLAY\r\nDESCRIPTION:Alarm2a\r\nTRIGGER:-PT30M\r\nEND:VALARM\r\n",
            [comp.to_ical() for comp in calendar.subcomponents[1].subcomponents],
        )
        self.assertIn(
            b"BEGIN:VALARM\r\nACTION:DISPLAY\r\nDESCRIPTION:Alarm2b\r\nTRIGGER:-P1D\r\nEND:VALARM\r\n",
            [comp.to_ical() for comp in calendar.subcomponents[1].subcomponents],
        )

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
        self.assertEqual(calendar["X-WR-TIMEZONE"], "Asia/Tokyo")

    def test_timezone(self):
        tokyo = pytz.timezone("Asia/Tokyo")
        us_eastern = pytz.timezone("US/Eastern")

        class TestTimezoneFeed(TestItemsFeed):
            def items(self):
                return [
                    {
                        "title": "Title1",
                        "description": "Description1",
                        "link": "/event/1",
                        "start": datetime(2012, 5, 1, 18, 00, tzinfo=tokyo),
                        "end": datetime(2012, 5, 1, 20, 00, tzinfo=tokyo),
                        "recurrences": {
                            "rrules": [],
                            "xrules": [],
                            "rdates": [],
                            "xdates": [],
                        },
                    },
                    {
                        "title": "Title2",
                        "description": "Description2",
                        "link": "/event/2",
                        "start": datetime(2012, 5, 6, 18, 00, tzinfo=us_eastern),
                        "end": datetime(2012, 5, 6, 20, 00, tzinfo=us_eastern),
                        "recurrences": {
                            "rrules": [],
                            "xrules": [],
                            "rdates": [],
                            "xdates": [],
                        },
                    },
                ]

        request = RequestFactory().get("/test/ical")
        view = TestTimezoneFeed()

        response = view(request)
        calendar = icalendar.Calendar.from_ical(response.content)
        self.assertEqual(len(calendar.subcomponents), 2)

        self.assertEqual(
            calendar.subcomponents[0]["DTSTART"].to_ical(), b"20120501T180000"
        )
        self.assertEqual(
            calendar.subcomponents[0]["DTSTART"].params["TZID"], "Asia/Tokyo"
        )

        self.assertEqual(
            calendar.subcomponents[0]["DTEND"].to_ical(), b"20120501T200000"
        )
        self.assertEqual(
            calendar.subcomponents[0]["DTEND"].params["TZID"], "Asia/Tokyo"
        )

        self.assertEqual(
            calendar.subcomponents[1]["DTSTART"].to_ical(), b"20120506T180000"
        )
        self.assertEqual(
            calendar.subcomponents[1]["DTSTART"].params["TZID"], "US/Eastern"
        )

        self.assertEqual(
            calendar.subcomponents[1]["DTEND"].to_ical(), b"20120506T200000"
        )
        self.assertEqual(
            calendar.subcomponents[1]["DTEND"].params["TZID"], "US/Eastern"
        )

    def test_file_name(self):
        request = RequestFactory().get("/test/ical")
        view = TestFilenameFeed()

        response = view(request)

        self.assertIn("Content-Disposition", response)
        self.assertEqual(
            response["content-disposition"], 'attachment; filename="123.ics"'
        )

    def test_file_type(self):
        request = RequestFactory().get("/test/ical")
        view = TestFilenameFeed()
        response = view(request)
        self.assertIn("Content-Type", response)
        self.assertEqual(
            response["content-type"],
            "text/calendar; charset=utf8",
        )

    def test_file_header(self):
        request = RequestFactory().get("/test/ical")
        view = TestFilenameFeed()
        response = view(request)
        header = b"BEGIN:VCALENDAR\r\nVERSION:2.0"
        self.assertTrue(response.content.startswith(header))
