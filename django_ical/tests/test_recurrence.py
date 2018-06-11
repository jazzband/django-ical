# -*- coding: utf-8 -*-
"""Test calendar rrules."""

# Future
from __future__ import absolute_import
from __future__ import unicode_literals

import datetime
import pytz

from django.test import TestCase

from django_ical import utils


class FromTextTests(TestCase):
    """Test build a vRecur dictionary from an RRULE string."""

    def test_every_day(self):
        """Repeat every day."""
        vrecurr = utils.build_rrule_from_text('FREQ=DAILY')
        assert vrecurr['FREQ'] == ['DAILY']
        assert len(vrecurr.keys()) == 1

    def test_daily_byhour(self):
        """Repeat every day at 10, 12 and 17."""
        vrecurr = utils.build_rrule_from_text('FREQ=DAILY;BYHOUR=10,12,17')
        assert vrecurr['FREQ'] == ['DAILY']
        assert vrecurr['BYHOUR'] == [10, 12, 17]
        assert len(vrecurr.keys()) == 2

    def test_every_week(self):
        """Repeat every week."""
        vrecurr = utils.build_rrule_from_text('FREQ=WEEKLY')
        assert vrecurr['FREQ'] == ['WEEKLY']
        assert len(vrecurr.keys()) == 1

    def test_ever_hour(self):
        """Repeat every hour."""
        vrecurr = utils.build_rrule_from_text('FREQ=HOURLY')
        assert vrecurr['FREQ'] == ['HOURLY']
        assert len(vrecurr.keys()) == 1

    def test_ever_4_hours(self):
        """Repeat every 4 hours."""
        vrecurr = utils.build_rrule_from_text('INTERVAL=4;FREQ=HOURLY')
        assert vrecurr['FREQ'] == ['HOURLY']
        assert vrecurr['INTERVAL'] == [4]
        assert len(vrecurr.keys()) == 2

    def test_weekly_tue(self):
        """Repeat every week on Tuesday."""
        vrecurr = utils.build_rrule_from_text('FREQ=WEEKLY;BYDAY=TU')
        assert vrecurr['FREQ'] == ['WEEKLY']
        assert vrecurr['BYDAY'] == ['TU']
        assert len(vrecurr.keys()) == 2

    def test_weekly_mo_wed(self):
        """Repeat every week on Monday, Wednesday."""
        vrecurr = utils.build_rrule_from_text('FREQ=WEEKLY;BYDAY=MO,WE')
        assert vrecurr['FREQ'] == ['WEEKLY']
        assert vrecurr['BYDAY'] == ['MO', 'WE']
        assert len(vrecurr.keys()) == 2

    def test_every_weekday(self):
        """Repeat every weekday."""
        vrecurr = utils.build_rrule_from_text('FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR')
        assert vrecurr['FREQ'] == ['WEEKLY']
        assert vrecurr['BYDAY'] == ['MO', 'TU', 'WE', 'TH', 'FR']
        assert len(vrecurr.keys()) == 2

    def test_every_2_weeks(self):
        """Repeat every 2 weeks."""
        vrecurr = utils.build_rrule_from_text('INTERVAL=2;FREQ=WEEKLY')
        assert vrecurr['FREQ'] == ['WEEKLY']
        assert vrecurr['INTERVAL'] == [2]
        assert len(vrecurr.keys()) == 2

    def test_every_month(self):
        """Repeat every month."""
        vrecurr = utils.build_rrule_from_text('FREQ=MONTHLY')
        assert vrecurr['FREQ'] == ['MONTHLY']
        assert len(vrecurr.keys()) == 1

    def test_every_6_months(self):
        """Repeat very 6 months."""
        vrecurr = utils.build_rrule_from_text('INTERVAL=6;FREQ=MONTHLY')
        assert vrecurr['FREQ'] == ['MONTHLY']
        assert vrecurr['INTERVAL'] == [6]
        assert len(vrecurr.keys()) == 2

    def test_every_year(self):
        """Repeat every year."""
        vrecurr = utils.build_rrule_from_text('FREQ=YEARLY')
        assert vrecurr['FREQ'] == ['YEARLY']
        assert len(vrecurr.keys()) == 1

    def test_every_month_on_the_4th(self):
        """Repeat every month on the 4th."""
        vrecurr = utils.build_rrule_from_text('FREQ=MONTHLY;BYMONTHDAY=4')
        assert vrecurr['FREQ'] == ['MONTHLY']
        assert vrecurr['BYMONTHDAY'] == [4]
        assert len(vrecurr.keys()) == 2
        vrecurr = utils.build_rrule_from_text('FREQ=MONTHLY;BYMONTHDAY=+4')
        assert vrecurr['FREQ'] == ['MONTHLY']
        assert vrecurr['BYMONTHDAY'] == [4]
        assert len(vrecurr.keys()) == 2

    def test_every_month_on_the_4th_last(self):
        """Repeat every month on the 4th last."""
        vrecurr = utils.build_rrule_from_text('FREQ=MONTHLY;BYMONTHDAY=-4')
        assert vrecurr['FREQ'] == ['MONTHLY']
        assert vrecurr['BYMONTHDAY'] == [-4]
        assert len(vrecurr.keys()) == 2

    def test_ever_month_3rd_tu(self):
        """Repeat every month on the 3rd Tuesday."""
        vrecurr = utils.build_rrule_from_text('FREQ=MONTHLY;BYDAY=+3TU')
        assert vrecurr['FREQ'] == ['MONTHLY']
        assert vrecurr['BYDAY'] == ['+3TU']
        assert len(vrecurr.keys()) == 2

    def test_ever_month_3rd_last_tu(self):
        """Repeat every month on the 3rd last Tuesday."""
        vrecurr = utils.build_rrule_from_text('FREQ=MONTHLY;BYDAY=-3TU')
        assert vrecurr['FREQ'] == ['MONTHLY']
        assert vrecurr['BYDAY'] == ['-3TU']
        assert len(vrecurr.keys()) == 2

    def test_ever_month_last_mo(self):
        """Repeat every month on the last Monday."""
        vrecurr = utils.build_rrule_from_text('FREQ=MONTHLY;BYDAY=-1MO')
        assert vrecurr['FREQ'] == ['MONTHLY']
        assert vrecurr['BYDAY'] == ['-1MO']
        assert len(vrecurr.keys()) == 2

    def test_ever_month_second_last_fr(self):
        """Repeat every month on the 2nd last Friday."""
        vrecurr = utils.build_rrule_from_text('FREQ=MONTHLY;BYDAY=-2FR')
        assert vrecurr['FREQ'] == ['MONTHLY']
        assert vrecurr['BYDAY'] == ['-2FR']
        assert len(vrecurr.keys()) == 2

    def test_every_week_until_jan_2007(self):
        """Repeat every week until January 1, 2007."""
        utc=pytz.UTC
        vrecurr = utils.build_rrule_from_text('FREQ=WEEKLY;UNTIL=20070101T000000Z')
        assert vrecurr['FREQ'] == ['WEEKLY']
        assert vrecurr['UNTIL'] == [datetime.datetime(2007, 1, 1, 0, 0, tzinfo=utc)]
        assert len(vrecurr.keys()) == 2

    def test_every_week_20_times(self):
        """Repeat every week for 20 times."""
        vrecurr = utils.build_rrule_from_text('FREQ=WEEKLY;COUNT=20')
        assert vrecurr['FREQ'] == ['WEEKLY']
        assert vrecurr['COUNT'] == [20]
        assert len(vrecurr.keys()) == 2

    def test_every_month_last_working_day(self):
        """Repeat the last working day of each month."""
        vrecurr = utils.build_rrule_from_text('FREQ=MONTHLY;BYDAY=MO,TU,WE,TH,FR;BYSETPOS=-1;')
        assert vrecurr['FREQ'] == ['MONTHLY']
        assert vrecurr['BYDAY'] == ['MO', 'TU', 'WE', 'TH', 'FR']
        assert vrecurr['BYSETPOS'] == [-1]
        assert len(vrecurr.keys()) == 3

    def test_ever_month_last_day(self):
        """Repeat the last day of each month."""
        vrecurr = utils.build_rrule_from_text('FREQ=MONTHLY;BYMONTHDAY=-1')
        assert vrecurr['FREQ'] == ['MONTHLY']
        assert vrecurr['BYMONTHDAY'] == [-1]
        assert len(vrecurr.keys()) == 2

    def test_every_day_in_jan(self):
        """Repeat every day in January"""
        vrecurr = utils.build_rrule_from_text('FREQ=YEARLY;BYMONTH=1;BYDAY=MO,TU,WE,TH,FR,SA,SU;')
        assert vrecurr['FREQ'] == ['YEARLY']
        assert vrecurr['BYMONTH'] == [1]
        assert vrecurr['BYDAY'] == ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']
        assert len(vrecurr.keys()) == 3

    def test_every_2nd_15th_of_month(self):
        """Repeat monthly on the 2nd and 15th of the month."""
        vrecurr = utils.build_rrule_from_text('FREQ=MONTHLY;BYMONTHDAY=4,15')
        assert vrecurr['FREQ'] == ['MONTHLY']
        assert vrecurr['BYMONTHDAY'] == [4, 15]
        assert len(vrecurr.keys()) == 2

    def test_every_fr_13th(self):
        """Repeat every Friday the 13th."""
        vrecurr = utils.build_rrule_from_text('FREQ=YEARLY;BYMONTHDAY=13;BYDAY=FR')
        assert vrecurr['FREQ'] == ['YEARLY']
        assert vrecurr['BYMONTHDAY'] == [13]
        assert vrecurr['BYDAY'] == ['FR']
        assert len(vrecurr.keys()) == 3
