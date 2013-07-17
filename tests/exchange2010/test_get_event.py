"""
(c) 2013 LinkedIn Corp. All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License");?you may not use this file except in compliance with the License. You may obtain a copy of the License at  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software?distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
import httpretty
from nose.tools import eq_, raises
from pyexchange import Exchange2010Service
from pyexchange.connection import ExchangeNTLMAuthConnection
from pyexchange.exceptions import *

from .fixtures import *

class Test_ParseEventResponseData(object):
  event = None

  @classmethod
  def setUpAll(cls):

    @httpretty.activate # this decorator doesn't play nice with @classmethod
    def fake_event_request():

      service = Exchange2010Service(connection=ExchangeNTLMAuthConnection(url=FAKE_EXCHANGE_URL, username=FAKE_EXCHANGE_USERNAME, password=FAKE_EXCHANGE_PASSWORD))

      httpretty.register_uri(httpretty.POST, FAKE_EXCHANGE_URL,
                                 body=GET_ITEM_RESPONSE.encode('utf-8'),
                                 content_type='text/xml; charset=utf-8')

      return service.calendar().get_event(id=TEST_EVENT.id)

    cls.event = fake_event_request()


  def test_canary(self):
    assert self.event is not None

  def test_event_id_was_not_changed(self):
    eq_(self.event.id, TEST_EVENT.id)

  def test_event_has_a_subject(self):
    eq_(self.event.subject, TEST_EVENT.subject)

  def test_event_has_a_location(self):
    eq_(self.event.location, TEST_EVENT.location)

  def test_event_has_a_body(self):
    eq_(self.event.html_body, TEST_EVENT.body)
    eq_(self.event.text_body, TEST_EVENT.body)
    eq_(self.event.body, TEST_EVENT.body)

  def test_event_starts_at_the_right_time(self):
    eq_(self.event.start, TEST_EVENT.start)

  def test_event_ends_at_the_right_time(self):
    eq_(self.event.end, TEST_EVENT.end)

  def test_event_has_an_organizer(self):
    assert self.event.organizer is not None
    eq_(self.event.organizer.name, ORGANIZER.name)
    eq_(self.event.organizer.email, ORGANIZER.email)

  def test_event_has_the_correct_attendees(self):
    assert len(self.event.attendees) > 0
    eq_(len(self.event.attendees), len(ATTENDEE_LIST))

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
    eq_(self.event.resources, [RESOURCE])

  def test_conference_room_alias(self):
    eq_(self.event.conference_room, RESOURCE)

  def test_required_attendees_are_required(self):
    eq_(sorted(self.event.required_attendees), sorted(REQUIRED_PEOPLE))

  def test_optional_attendees_are_optional(self):
    eq_(sorted(self.event.optional_attendees), sorted(OPTIONAL_PEOPLE))


class Test_FailingToGetEvents():

  service = None

  @classmethod
  def setUpAll(cls):

    cls.service = Exchange2010Service(connection=ExchangeNTLMAuthConnection(url=FAKE_EXCHANGE_URL,
                                                                        username=FAKE_EXCHANGE_USERNAME,
                                                                        password=FAKE_EXCHANGE_PASSWORD))

  @raises(ExchangeItemNotFoundException)
  @httpretty.activate
  def test_requesting_an_event_id_that_doest_exist_throws_exception(self):

    httpretty.register_uri(httpretty.POST, FAKE_EXCHANGE_URL,
                                 body=ITEM_DOES_NOT_EXIST.encode('utf-8'),
                                 content_type='text/xml; charset=utf-8')

    self.service.calendar().get_event(id=TEST_EVENT.id)


  @raises(FailedExchangeException)
  @httpretty.activate
  def test_requesting_an_event_and_getting_a_500_response_throws_exception(self):

    httpretty.register_uri(httpretty.POST, FAKE_EXCHANGE_URL,
                                 body=u"",
                                 status=500,
                                 content_type='text/xml; charset=utf-8')

    self.service.calendar().get_event(id=TEST_EVENT.id)





