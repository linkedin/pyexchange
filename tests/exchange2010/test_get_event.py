"""
(c) 2013 LinkedIn Corp. All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License");?you may not use this file except in compliance with the License. You may obtain a copy of the License at  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software?distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
from httpretty import HTTPretty, httprettified, activate
import unittest
from pytest import raises
from pyexchange import Exchange2010Service
from pyexchange.connection import ExchangeNTLMAuthConnection
from pyexchange.exceptions import *  # noqa

from .fixtures import *  # noqa


class Test_ParseEventResponseData(unittest.TestCase):
  event = None

  @classmethod
  def setUpClass(cls):

    @activate  # this decorator doesn't play nice with @classmethod
    def fake_event_request():

      service = Exchange2010Service(
        connection=ExchangeNTLMAuthConnection(
          url=FAKE_EXCHANGE_URL, username=FAKE_EXCHANGE_USERNAME, password=FAKE_EXCHANGE_PASSWORD
        )
      )

      HTTPretty.register_uri(
        HTTPretty.POST, FAKE_EXCHANGE_URL,
        body=GET_ITEM_RESPONSE.encode('utf-8'),
        content_type='text/xml; charset=utf-8',
      )

      return service.calendar().get_event(id=TEST_EVENT.id)

    cls.event = fake_event_request()

  def test_canary(self):
    assert self.event is not None

  def test_event_id_was_not_changed(self):
    assert self.event.id == TEST_EVENT.id

  def test_event_has_a_subject(self):
    assert self.event.subject == TEST_EVENT.subject

  def test_event_has_a_location(self):
    assert self.event.location == TEST_EVENT.location

  def test_event_has_a_body(self):
    assert self.event.html_body == TEST_EVENT.body
    assert self.event.text_body == TEST_EVENT.body
    assert self.event.body == TEST_EVENT.body

  def test_event_starts_at_the_right_time(self):
    assert self.event.start == TEST_EVENT.start

  def test_event_ends_at_the_right_time(self):
    assert self.event.end == TEST_EVENT.end

  def test_event_has_an_organizer(self):
    assert self.event.organizer is not None
    assert self.event.organizer.name == ORGANIZER.name
    assert self.event.organizer.email == ORGANIZER.email

  def test_event_has_the_correct_attendees(self):
    assert len(self.event.attendees) > 0
    assert len(self.event.attendees) == len(ATTENDEE_LIST)

  def _test_person_values_are_correct(self, fixture):

    try:
      self.event.attendees.index(fixture)
    except ValueError as e:
      print(u"An attendee should be in the list but isn't:", fixture)
      raise e

  def test_all_attendees_are_present_and_accounted_for(self):

    # this is a nose test generator if you haven't seen one before
    # it creates one test for each attendee
    for attendee in ATTENDEE_LIST:
      yield self._test_person_values_are_correct, attendee

  def test_resources_are_correct(self):
    assert self.event.resources == [RESOURCE]

  def test_conference_room_alias(self):
    assert self.event.conference_room == RESOURCE

  def test_required_attendees_are_required(self):
    assert sorted(self.event.required_attendees) == sorted(REQUIRED_PEOPLE)

  def test_optional_attendees_are_optional(self):
    assert sorted(self.event.optional_attendees) == sorted(OPTIONAL_PEOPLE)


class Test_FailingToGetEvents(unittest.TestCase):

  service = None

  @classmethod
  def setUpClass(cls):

    cls.service = Exchange2010Service(
      connection=ExchangeNTLMAuthConnection(
        url=FAKE_EXCHANGE_URL, username=FAKE_EXCHANGE_USERNAME, password=FAKE_EXCHANGE_PASSWORD
      )
    )

  @activate
  def test_requesting_an_event_id_that_doest_exist_throws_exception(self):

    HTTPretty.register_uri(
      HTTPretty.POST, FAKE_EXCHANGE_URL,
      body=ITEM_DOES_NOT_EXIST.encode('utf-8'),
      content_type='text/xml; charset=utf-8',
    )

    with raises(ExchangeItemNotFoundException):
      self.service.calendar().get_event(id=TEST_EVENT.id)

  @activate
  def test_requesting_an_event_and_getting_a_500_response_throws_exception(self):

    HTTPretty.register_uri(
      HTTPretty.POST, FAKE_EXCHANGE_URL,
      body=u"",
      status=500,
      content_type='text/xml; charset=utf-8',
    )

    with raises(FailedExchangeException):
     self.service.calendar().get_event(id=TEST_EVENT.id)


class Test_GetRecurringMasterEvents(unittest.TestCase):
  service = None
  event = None

  @classmethod
  def setUpClass(cls):
    cls.service = Exchange2010Service(
      connection=ExchangeNTLMAuthConnection(
        url=FAKE_EXCHANGE_URL,
        username=FAKE_EXCHANGE_USERNAME,
        password=FAKE_EXCHANGE_PASSWORD
      )
    )

  @httprettified
  def test_get_recurring_daily_event(self):
    HTTPretty.register_uri(
      HTTPretty.POST, FAKE_EXCHANGE_URL,
      body=GET_RECURRING_MASTER_DAILY_EVENT.encode('utf-8'),
      content_type='text/xml; charset=utf-8',
    )
    event = self.service.calendar(id=TEST_RECURRING_EVENT_DAILY.calendar_id).get_event(
      id=TEST_RECURRING_EVENT_DAILY.id
    )
    assert event.id == TEST_RECURRING_EVENT_DAILY.id
    assert event.calendar_id == TEST_RECURRING_EVENT_DAILY.calendar_id
    assert event.subject == TEST_RECURRING_EVENT_DAILY.subject
    assert event.location == TEST_RECURRING_EVENT_DAILY.location
    assert event.start == TEST_RECURRING_EVENT_DAILY.start
    assert event.end == TEST_RECURRING_EVENT_DAILY.end
    assert event.body == TEST_RECURRING_EVENT_DAILY.body
    assert event.html_body == TEST_RECURRING_EVENT_DAILY.body
    assert event.recurrence == 'daily'
    assert event.recurrence_interval == TEST_RECURRING_EVENT_DAILY.recurrence_interval
    assert event.recurrence_end_date == TEST_RECURRING_EVENT_DAILY.recurrence_end_date

  @httprettified
  def test_get_recurring_weekly_event(self):
    HTTPretty.register_uri(
      HTTPretty.POST, FAKE_EXCHANGE_URL,
      body=GET_RECURRING_MASTER_WEEKLY_EVENT.encode('utf-8'),
      content_type='text/xml; charset=utf-8',
    )
    event = self.service.calendar(id=TEST_RECURRING_EVENT_WEEKLY.calendar_id).get_event(
      id=TEST_RECURRING_EVENT_WEEKLY.id
    )
    assert event.id == TEST_RECURRING_EVENT_WEEKLY.id
    assert event.calendar_id == TEST_RECURRING_EVENT_WEEKLY.calendar_id
    assert event.subject == TEST_RECURRING_EVENT_WEEKLY.subject
    assert event.location == TEST_RECURRING_EVENT_WEEKLY.location
    assert event.start == TEST_RECURRING_EVENT_WEEKLY.start
    assert event.end == TEST_RECURRING_EVENT_WEEKLY.end
    assert event.body == TEST_RECURRING_EVENT_WEEKLY.body
    assert event.html_body == TEST_RECURRING_EVENT_WEEKLY.body
    assert event.recurrence == 'weekly'
    assert event.recurrence_interval == TEST_RECURRING_EVENT_WEEKLY.recurrence_interval
    assert event.recurrence_end_date == TEST_RECURRING_EVENT_WEEKLY.recurrence_end_date

  @httprettified
  def test_get_recurring_monthly_event(self):
    HTTPretty.register_uri(
      HTTPretty.POST, FAKE_EXCHANGE_URL,
      body=GET_RECURRING_MASTER_MONTHLY_EVENT.encode('utf-8'),
      content_type='text/xml; charset=utf-8',
    )
    event = self.service.calendar(id=TEST_RECURRING_EVENT_MONTHLY.calendar_id).get_event(
      id=TEST_RECURRING_EVENT_MONTHLY.id
    )
    assert event.id == TEST_RECURRING_EVENT_MONTHLY.id
    assert event.calendar_id == TEST_RECURRING_EVENT_MONTHLY.calendar_id
    assert event.subject == TEST_RECURRING_EVENT_MONTHLY.subject
    assert event.location == TEST_RECURRING_EVENT_MONTHLY.location
    assert event.start == TEST_RECURRING_EVENT_MONTHLY.start
    assert event.end == TEST_RECURRING_EVENT_MONTHLY.end
    assert event.body == TEST_RECURRING_EVENT_MONTHLY.body
    assert event.html_body == TEST_RECURRING_EVENT_MONTHLY.body
    assert event.recurrence == 'monthly'
    assert event.recurrence_interval == TEST_RECURRING_EVENT_MONTHLY.recurrence_interval
    assert event.recurrence_end_date == TEST_RECURRING_EVENT_MONTHLY.recurrence_end_date

  @httprettified
  def test_get_recurring_yearly_event(self):
    HTTPretty.register_uri(
      HTTPretty.POST, FAKE_EXCHANGE_URL,
      body=GET_RECURRING_MASTER_YEARLY_EVENT.encode('utf-8'),
      content_type='text/xml; charset=utf-8',
    )
    event = self.service.calendar(id=TEST_RECURRING_EVENT_YEARLY.calendar_id).get_event(
      id=TEST_RECURRING_EVENT_YEARLY.id
    )
    assert event.id == TEST_RECURRING_EVENT_YEARLY.id
    assert event.calendar_id == TEST_RECURRING_EVENT_YEARLY.calendar_id
    assert event.subject == TEST_RECURRING_EVENT_YEARLY.subject
    assert event.location == TEST_RECURRING_EVENT_YEARLY.location
    assert event.start == TEST_RECURRING_EVENT_YEARLY.start
    assert event.end == TEST_RECURRING_EVENT_YEARLY.end
    assert event.body == TEST_RECURRING_EVENT_YEARLY.body
    assert event.html_body == TEST_RECURRING_EVENT_YEARLY.body
    assert event.recurrence == 'yearly'
    assert event.recurrence_end_date == TEST_RECURRING_EVENT_YEARLY.recurrence_end_date
