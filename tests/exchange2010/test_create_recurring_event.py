"""
(c) 2013 LinkedIn Corp. All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License");?you may not use this file except in compliance with the License. You may obtain a copy of the License at  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software?distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
from httpretty import HTTPretty, httprettified
from nose.tools import eq_, raises
from pyexchange import Exchange2010Service

from pyexchange.connection import ExchangeNTLMAuthConnection
from pyexchange.exceptions import *  # noqa

from .fixtures import *  # noqa


class Test_PopulatingANewRecurringDailyEvent():
  """ Tests all the attribute setting works when creating a new event """
  calendar = None

  @classmethod
  def setUpAll(cls):

    cls.calendar = Exchange2010Service(
      connection=ExchangeNTLMAuthConnection(
        url=FAKE_EXCHANGE_URL,
        username=FAKE_EXCHANGE_USERNAME,
        password=FAKE_EXCHANGE_PASSWORD,
      )
    ).calendar()

  def test_can_set_recurring(self):
    event = self.calendar.event(
      recurrence=TEST_RECURRING_EVENT_DAILY.recurrence,
      recurrence_interval=TEST_RECURRING_EVENT_DAILY.recurrence_interval,
      recurrence_end_date=TEST_RECURRING_EVENT_DAILY.recurrence_end_date,
    )
    eq_(event.recurrence, TEST_RECURRING_EVENT_DAILY.recurrence)
    eq_(event.recurrence_interval, TEST_RECURRING_EVENT_DAILY.recurrence_interval)
    eq_(event.recurrence_end_date, TEST_RECURRING_EVENT_DAILY.recurrence_end_date)


class Test_CreatingANewRecurringDailyEvent(object):
  service = None
  event = None

  @classmethod
  def setUpAll(cls):
    cls.service = Exchange2010Service(
      connection=ExchangeNTLMAuthConnection(
        url=FAKE_EXCHANGE_URL,
        username=FAKE_EXCHANGE_USERNAME,
        password=FAKE_EXCHANGE_PASSWORD
      )
    )

  def setUp(self):
    self.event = self.service.calendar().event(
      subject=TEST_RECURRING_EVENT_DAILY.subject,
      start=TEST_RECURRING_EVENT_DAILY.start,
      end=TEST_RECURRING_EVENT_DAILY.end,
      recurrence=TEST_RECURRING_EVENT_DAILY.recurrence,
      recurrence_interval=TEST_RECURRING_EVENT_DAILY.recurrence_interval,
      recurrence_end_date=TEST_RECURRING_EVENT_DAILY.recurrence_end_date,
    )

  @raises(ValueError)
  def test_recurrence_must_have_interval(self):
    self.event.recurrence_interval = None
    self.event.create()

  @raises(ValueError)
  def test_recurrence_interval_low_value(self):
    self.event.recurrence_interval = 0
    self.event.create()

  @raises(ValueError)
  def test_recurrence_interval_high_value(self):
    self.event.recurrence_interval = 1000
    self.event.create()

  @httprettified
  def test_recurrence_interval_min_value(self):
    HTTPretty.register_uri(
      HTTPretty.POST, FAKE_EXCHANGE_URL,
      body=CREATE_ITEM_RESPONSE.encode('utf-8'),
      content_type='text/xml; charset=utf-8',
    )
    self.event.recurrence_interval = 1
    self.event.create()
    eq_(self.event.id, TEST_RECURRING_EVENT_DAILY.id)

  @httprettified
  def test_recurrence_interval_max_value(self):
    HTTPretty.register_uri(
      HTTPretty.POST, FAKE_EXCHANGE_URL,
      body=CREATE_ITEM_RESPONSE.encode('utf-8'),
      content_type='text/xml; charset=utf-8',
    )
    self.event.recurrence_interval = 999
    self.event.create()
    eq_(self.event.id, TEST_RECURRING_EVENT_DAILY.id)

  @raises(ValueError)
  def test_recurrence_must_have_end_date(self):
    self.event.recurrence_end_date = None
    self.event.create()

  @raises(ValueError)
  def test_recurrence_end_before_start(self):
    self.event.recurrence_end_date = self.event.start.date() - timedelta(1)
    self.event.create()

  @httprettified
  def test_create_recurrence_daily(self):
    HTTPretty.register_uri(
      HTTPretty.POST, FAKE_EXCHANGE_URL,
      body=CREATE_ITEM_RESPONSE.encode('utf-8'),
      content_type='text/xml; charset=utf-8',
    )
    self.event.create()
    eq_(self.event.id, TEST_RECURRING_EVENT_DAILY.id)


class Test_PopulatingANewRecurringWeeklyEvent():
  """ Tests all the attribute setting works when creating a new event """
  calendar = None

  @classmethod
  def setUpAll(cls):

    cls.calendar = Exchange2010Service(
      connection=ExchangeNTLMAuthConnection(
        url=FAKE_EXCHANGE_URL,
        username=FAKE_EXCHANGE_USERNAME,
        password=FAKE_EXCHANGE_PASSWORD,
      )
    ).calendar()

  def test_can_set_recurring(self):
    event = self.calendar.event(
      recurrence=TEST_RECURRING_EVENT_WEEKLY.recurrence,
      recurrence_interval=TEST_RECURRING_EVENT_WEEKLY.recurrence_interval,
      recurrence_end_date=TEST_RECURRING_EVENT_WEEKLY.recurrence_end_date,
      recurrence_days=TEST_RECURRING_EVENT_WEEKLY.recurrence_days,
    )
    eq_(event.recurrence, TEST_RECURRING_EVENT_WEEKLY.recurrence)
    eq_(event.recurrence_interval, TEST_RECURRING_EVENT_WEEKLY.recurrence_interval)
    eq_(event.recurrence_end_date, TEST_RECURRING_EVENT_WEEKLY.recurrence_end_date)
    eq_(event.recurrence_days, TEST_RECURRING_EVENT_WEEKLY.recurrence_days)


class Test_CreatingANewRecurringWeeklyEvent(object):
  service = None
  event = None

  @classmethod
  def setUpAll(cls):
    cls.service = Exchange2010Service(
      connection=ExchangeNTLMAuthConnection(
        url=FAKE_EXCHANGE_URL,
        username=FAKE_EXCHANGE_USERNAME,
        password=FAKE_EXCHANGE_PASSWORD
      )
    )

  def setUp(self):
    self.event = self.service.calendar().event(
      subject=TEST_RECURRING_EVENT_WEEKLY.subject,
      start=TEST_RECURRING_EVENT_WEEKLY.start,
      end=TEST_RECURRING_EVENT_WEEKLY.end,
      recurrence=TEST_RECURRING_EVENT_WEEKLY.recurrence,
      recurrence_interval=TEST_RECURRING_EVENT_WEEKLY.recurrence_interval,
      recurrence_end_date=TEST_RECURRING_EVENT_WEEKLY.recurrence_end_date,
      recurrence_days=TEST_RECURRING_EVENT_WEEKLY.recurrence_days,
    )

  @raises(ValueError)
  def test_recurrence_must_have_interval(self):
    self.event.recurrence_interval = None
    self.event.create()

  @raises(ValueError)
  def test_recurrence_interval_low_value(self):
    self.event.recurrence_interval = 0
    self.event.create()

  @raises(ValueError)
  def test_recurrence_interval_high_value(self):
    self.event.recurrence_interval = 100
    self.event.create()

  @httprettified
  def test_recurrence_interval_min_value(self):
    HTTPretty.register_uri(
      HTTPretty.POST, FAKE_EXCHANGE_URL,
      body=CREATE_ITEM_RESPONSE.encode('utf-8'),
      content_type='text/xml; charset=utf-8',
    )
    self.event.recurrence_interval = 1
    self.event.create()
    eq_(self.event.id, TEST_RECURRING_EVENT_WEEKLY.id)

  @httprettified
  def test_recurrence_interval_max_value(self):
    HTTPretty.register_uri(
      HTTPretty.POST, FAKE_EXCHANGE_URL,
      body=CREATE_ITEM_RESPONSE.encode('utf-8'),
      content_type='text/xml; charset=utf-8',
    )
    self.event.recurrence_interval = 99
    self.event.create()
    eq_(self.event.id, TEST_RECURRING_EVENT_WEEKLY.id)

  @raises(ValueError)
  def test_recurrence_must_have_end_date(self):
    self.event.recurrence_end_date = None
    self.event.create()

  @raises(ValueError)
  def test_recurrence_end_before_start(self):
    self.event.recurrence_end_date = self.event.start.date() - timedelta(1)
    self.event.create()

  @raises(ValueError)
  def test_recurrence_bad_day(self):
    self.event.recurrence_days = 'Mondays'
    self.event.create()

  @raises(ValueError)
  def test_recurrence_no_day(self):
    self.event.recurrence_days = None
    self.event.create()

  @httprettified
  def test_create_recurrence_weekly(self):
    HTTPretty.register_uri(
      HTTPretty.POST, FAKE_EXCHANGE_URL,
      body=CREATE_ITEM_RESPONSE.encode('utf-8'),
      content_type='text/xml; charset=utf-8',
    )
    self.event.create()
    eq_(self.event.id, TEST_RECURRING_EVENT_WEEKLY.id)


class Test_PopulatingANewRecurringMonthlyEvent():
  """ Tests all the attribute setting works when creating a new event """
  calendar = None

  @classmethod
  def setUpAll(cls):

    cls.calendar = Exchange2010Service(
      connection=ExchangeNTLMAuthConnection(
        url=FAKE_EXCHANGE_URL,
        username=FAKE_EXCHANGE_USERNAME,
        password=FAKE_EXCHANGE_PASSWORD,
      )
    ).calendar()

  def test_can_set_recurring(self):
    event = self.calendar.event(
      recurrence=TEST_RECURRING_EVENT_MONTHLY.recurrence,
      recurrence_interval=TEST_RECURRING_EVENT_MONTHLY.recurrence_interval,
      recurrence_end_date=TEST_RECURRING_EVENT_MONTHLY.recurrence_end_date,
    )
    eq_(event.recurrence, TEST_RECURRING_EVENT_MONTHLY.recurrence)
    eq_(event.recurrence_interval, TEST_RECURRING_EVENT_MONTHLY.recurrence_interval)
    eq_(event.recurrence_end_date, TEST_RECURRING_EVENT_MONTHLY.recurrence_end_date)


class Test_CreatingANewRecurringMonthlyEvent(object):
  service = None
  event = None

  @classmethod
  def setUpAll(cls):
    cls.service = Exchange2010Service(
      connection=ExchangeNTLMAuthConnection(
        url=FAKE_EXCHANGE_URL,
        username=FAKE_EXCHANGE_USERNAME,
        password=FAKE_EXCHANGE_PASSWORD
      )
    )

  def setUp(self):
    self.event = self.service.calendar().event(
      subject=TEST_RECURRING_EVENT_MONTHLY.subject,
      start=TEST_RECURRING_EVENT_MONTHLY.start,
      end=TEST_RECURRING_EVENT_MONTHLY.end,
      recurrence=TEST_RECURRING_EVENT_MONTHLY.recurrence,
      recurrence_interval=TEST_RECURRING_EVENT_MONTHLY.recurrence_interval,
      recurrence_end_date=TEST_RECURRING_EVENT_MONTHLY.recurrence_end_date,
    )

  @raises(ValueError)
  def test_recurrence_must_have_interval(self):
    self.event.recurrence_interval = None
    self.event.create()

  @raises(ValueError)
  def test_recurrence_interval_low_value(self):
    self.event.recurrence_interval = 0
    self.event.create()

  @raises(ValueError)
  def test_recurrence_interval_high_value(self):
    self.event.recurrence_interval = 100
    self.event.create()

  @httprettified
  def test_recurrence_interval_min_value(self):
    HTTPretty.register_uri(
      HTTPretty.POST, FAKE_EXCHANGE_URL,
      body=CREATE_ITEM_RESPONSE.encode('utf-8'),
      content_type='text/xml; charset=utf-8',
    )
    self.event.recurrence_interval = 1
    self.event.create()
    eq_(self.event.id, TEST_RECURRING_EVENT_MONTHLY.id)

  @httprettified
  def test_recurrence_interval_max_value(self):
    HTTPretty.register_uri(
      HTTPretty.POST, FAKE_EXCHANGE_URL,
      body=CREATE_ITEM_RESPONSE.encode('utf-8'),
      content_type='text/xml; charset=utf-8',
    )
    self.event.recurrence_interval = 99
    self.event.create()
    eq_(self.event.id, TEST_RECURRING_EVENT_MONTHLY.id)

  @raises(ValueError)
  def test_recurrence_must_have_end_date(self):
    self.event.recurrence_end_date = None
    self.event.create()

  @raises(ValueError)
  def test_recurrence_end_before_start(self):
    self.event.recurrence_end_date = self.event.start.date() - timedelta(1)
    self.event.create()

  @httprettified
  def test_create_recurrence_monthly(self):
    HTTPretty.register_uri(
      HTTPretty.POST, FAKE_EXCHANGE_URL,
      body=CREATE_ITEM_RESPONSE.encode('utf-8'),
      content_type='text/xml; charset=utf-8',
    )
    self.event.create()
    eq_(self.event.id, TEST_RECURRING_EVENT_MONTHLY.id)


class Test_PopulatingANewRecurringYearlyEvent():
  """ Tests all the attribute setting works when creating a new event """
  calendar = None

  @classmethod
  def setUpAll(cls):

    cls.calendar = Exchange2010Service(
      connection=ExchangeNTLMAuthConnection(
        url=FAKE_EXCHANGE_URL,
        username=FAKE_EXCHANGE_USERNAME,
        password=FAKE_EXCHANGE_PASSWORD,
      )
    ).calendar()

  def test_can_set_recurring(self):
    event = self.calendar.event(
      recurrence=TEST_RECURRING_EVENT_YEARLY.recurrence,
      recurrence_end_date=TEST_RECURRING_EVENT_YEARLY.recurrence_end_date,
    )
    eq_(event.recurrence, TEST_RECURRING_EVENT_YEARLY.recurrence)
    eq_(event.recurrence_end_date, TEST_RECURRING_EVENT_YEARLY.recurrence_end_date)


class Test_CreatingANewRecurringYearlyEvent(object):
  service = None
  event = None

  @classmethod
  def setUpAll(cls):
    cls.service = Exchange2010Service(
      connection=ExchangeNTLMAuthConnection(
        url=FAKE_EXCHANGE_URL,
        username=FAKE_EXCHANGE_USERNAME,
        password=FAKE_EXCHANGE_PASSWORD
      )
    )

  def setUp(self):
    self.event = self.service.calendar().event(
      subject=TEST_RECURRING_EVENT_YEARLY.subject,
      start=TEST_RECURRING_EVENT_YEARLY.start,
      end=TEST_RECURRING_EVENT_YEARLY.end,
      recurrence=TEST_RECURRING_EVENT_YEARLY.recurrence,
      recurrence_end_date=TEST_RECURRING_EVENT_YEARLY.recurrence_end_date,
    )

  @raises(ValueError)
  def test_recurrence_must_have_end_date(self):
    self.event.recurrence_end_date = None
    self.event.create()

  @raises(ValueError)
  def test_recurrence_end_before_start(self):
    self.event.recurrence_end_date = self.event.start.date() - timedelta(1)
    self.event.create()

  @httprettified
  def test_create_recurrence_yearly(self):
    HTTPretty.register_uri(
      HTTPretty.POST, FAKE_EXCHANGE_URL,
      body=CREATE_ITEM_RESPONSE.encode('utf-8'),
      content_type='text/xml; charset=utf-8',
    )
    self.event.create()
    eq_(self.event.id, TEST_RECURRING_EVENT_YEARLY.id)
