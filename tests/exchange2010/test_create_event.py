"""
(c) 2013 LinkedIn Corp. All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License");?you may not use this file except in compliance with the License. You may obtain a copy of the License at  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software?distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
from httpretty import HTTPretty, httprettified
from nose.tools import eq_, raises
from pyexchange import Exchange2010Service

from pyexchange.connection import ExchangeNTLMAuthConnection
from pyexchange.base.calendar import ExchangeEventAttendee
from pyexchange.exceptions import *

from .fixtures import *
from .. import wip

class Test_PopulatingANewEvent():
  """ Tests all the attribute setting works when creating a new event """
  calendar = None

  @classmethod
  def setUpAll(cls):

    cls.calendar =  Exchange2010Service(connection=ExchangeNTLMAuthConnection(url=FAKE_EXCHANGE_URL,
                                                                          username=FAKE_EXCHANGE_USERNAME,
                                                                          password=FAKE_EXCHANGE_PASSWORD)
                                    ).calendar()

  def test_canary(self):
    event = self.calendar.event()
    assert event is not None

  def test_events_created_dont_have_an_id(self):
    event = self.calendar.event()
    eq_(event.id, None)

  def test_can_add_a_subject(self):
    event = self.calendar.event(subject=TEST_EVENT.subject)
    eq_(event.subject, TEST_EVENT.subject)

  def test_can_add_a_location(self):
    event = self.calendar.event(location=TEST_EVENT.location)
    eq_(event.location, TEST_EVENT.location)

  def test_can_add_an_html_body(self):
    event = self.calendar.event(html_body=TEST_EVENT.body)
    eq_(event.html_body, TEST_EVENT.body)
    eq_(event.text_body, None)
    eq_(event.body, TEST_EVENT.body)

  def test_can_add_a_text_body(self):
    event = self.calendar.event(text_body=TEST_EVENT.body)
    eq_(event.text_body, TEST_EVENT.body)
    eq_(event.html_body, None)
    eq_(event.body, TEST_EVENT.body)

  def test_can_add_a_start_time(self):
    event = self.calendar.event(start=TEST_EVENT.start)
    eq_(event.start, TEST_EVENT.start)

  def test_can_add_an_end_time(self):
    event = self.calendar.event(end=TEST_EVENT.end)
    eq_(event.end, TEST_EVENT.end)

  def test_can_add_attendees_via_email(self):
    event = self.calendar.event(attendees=PERSON_REQUIRED_ACCEPTED.email)
    eq_(len(event.attendees), 1)
    eq_(len(event.required_attendees), 1)
    eq_(len(event.optional_attendees), 0)
    eq_(event.attendees[0].email, PERSON_REQUIRED_ACCEPTED.email)

  def test_can_add_multiple_attendees_via_email(self):
    event = self.calendar.event(attendees=[PERSON_REQUIRED_ACCEPTED.email, PERSON_REQUIRED_TENTATIVE.email])
    eq_(len(event.attendees), 2)
    eq_(len(event.required_attendees), 2)
    eq_(len(event.optional_attendees), 0)

  def test_can_add_attendees_via_named_tuple(self):

    person = ExchangeEventAttendee(name=PERSON_OPTIONAL_ACCEPTED.name, email=PERSON_OPTIONAL_ACCEPTED.email, required=PERSON_OPTIONAL_ACCEPTED.required)

    event = self.calendar.event(attendees=person)
    eq_(len(event.attendees), 1)
    eq_(len(event.required_attendees), 0)
    eq_(len(event.optional_attendees), 1)
    eq_(event.attendees[0].email, PERSON_OPTIONAL_ACCEPTED.email)

  def test_can_assign_to_required_attendees(self):

    event = self.calendar.event(attendees=PERSON_REQUIRED_ACCEPTED.email)
    event.required_attendees = [PERSON_REQUIRED_ACCEPTED.email, PERSON_OPTIONAL_ACCEPTED.email]

    eq_(len(event.attendees), 2)
    eq_(len(event.required_attendees), 2)
    eq_(len(event.optional_attendees), 0)

  def test_can_assign_to_optional_attendees(self):

    event = self.calendar.event(attendees=PERSON_REQUIRED_ACCEPTED.email)
    event.optional_attendees = PERSON_OPTIONAL_ACCEPTED.email

    eq_(len(event.attendees), 2)
    eq_(len(event.required_attendees), 1)
    eq_(len(event.optional_attendees), 1)
    eq_(event.required_attendees[0].email, PERSON_REQUIRED_ACCEPTED.email)
    eq_(event.optional_attendees[0].email, PERSON_OPTIONAL_ACCEPTED.email)


  def test_can_add_resources(self):
    event = self.calendar.event(resources=[RESOURCE.email])
    eq_(len(event.resources), 1)
    eq_(event.resources[0].email, RESOURCE.email)
    eq_(event.conference_room.email, RESOURCE.email)


class Test_CreatingANewEvent(object):
  service = None
  event = None

  @classmethod
  def setUpAll(cls):
    cls.service = Exchange2010Service(connection=ExchangeNTLMAuthConnection(url=FAKE_EXCHANGE_URL, username=FAKE_EXCHANGE_USERNAME, password=FAKE_EXCHANGE_PASSWORD))

  def setUp(self):
    self.event = self.service.calendar().event(start=TEST_EVENT.start, end=TEST_EVENT.end)

  @raises(ValueError)
  def test_events_must_have_a_start_date(self):
    self.event.start = None
    self.event.create()

  @raises(ValueError)
  def test_events_must_have_an_end_date(self):
    self.event.end = None
    self.event.create()

  @raises(ValueError)
  def test_event_end_date_must_come_after_start_date(self):
    self.event.start, self.event.end = self.event.end, self.event.start
    self.event.create()

  @raises(ValueError)
  def cant_delete_a_newly_created_event(self):
    self.event.delete()

  @raises(ValueError)
  def cant_update_a_newly_created_event(self):
    self.event.update()

  @raises(ValueError)
  def cant_resend_invites_for_a_newly_created_event(self):
    self.event.resend_invitations()

  @httprettified
  def test_can_set_subject(self):

    HTTPretty.register_uri(HTTPretty.POST, FAKE_EXCHANGE_URL,
                             body=CREATE_ITEM_RESPONSE.encode('utf-8'),
                             content_type='text/xml; charset=utf-8')

    self.event.subject = TEST_EVENT.subject
    self.event.create()

    assert TEST_EVENT.subject in HTTPretty.last_request.body.decode('utf-8')

  @httprettified
  def test_can_set_location(self):

    HTTPretty.register_uri(HTTPretty.POST, FAKE_EXCHANGE_URL,
                             body=CREATE_ITEM_RESPONSE.encode('utf-8'),
                             content_type='text/xml; charset=utf-8')

    self.event.location = TEST_EVENT.location
    self.event.create()

    assert TEST_EVENT.location in HTTPretty.last_request.body.decode('utf-8')

  @httprettified
  def test_can_set_html_body(self):

    HTTPretty.register_uri(HTTPretty.POST, FAKE_EXCHANGE_URL,
                             body=CREATE_ITEM_RESPONSE.encode('utf-8'),
                             content_type='text/xml; charset=utf-8')

    self.event.html_body = TEST_EVENT.body
    self.event.create()

    assert TEST_EVENT.body in HTTPretty.last_request.body.decode('utf-8')

  @httprettified
  def test_can_set_text_body(self):

    HTTPretty.register_uri(HTTPretty.POST, FAKE_EXCHANGE_URL,
                             body=CREATE_ITEM_RESPONSE.encode('utf-8'),
                             content_type='text/xml; charset=utf-8')

    self.event.text_body = TEST_EVENT.body
    self.event.create()

    assert TEST_EVENT.body in HTTPretty.last_request.body.decode('utf-8')

  @httprettified
  def test_start_time(self):

    HTTPretty.register_uri(HTTPretty.POST, FAKE_EXCHANGE_URL,
                             body=CREATE_ITEM_RESPONSE.encode('utf-8'),
                             content_type='text/xml; charset=utf-8')

    self.event.create()

    assert TEST_EVENT.start.strftime(EXCHANGE_DATE_FORMAT) in HTTPretty.last_request.body.decode('utf-8')

  @httprettified
  def test_end_time(self):

    HTTPretty.register_uri(HTTPretty.POST, FAKE_EXCHANGE_URL,
                             body=CREATE_ITEM_RESPONSE.encode('utf-8'),
                             content_type='text/xml; charset=utf-8')

    self.event.create()

    assert TEST_EVENT.end.strftime(EXCHANGE_DATE_FORMAT) in HTTPretty.last_request.body.decode('utf-8')

  @httprettified
  def test_attendees(self):

    HTTPretty.register_uri(HTTPretty.POST, FAKE_EXCHANGE_URL,
                             body=CREATE_ITEM_RESPONSE.encode('utf-8'),
                             content_type='text/xml; charset=utf-8')

    attendees = [PERSON_REQUIRED_ACCEPTED.email, PERSON_REQUIRED_TENTATIVE.email]

    self.event.attendees = attendees
    self.event.create()

    for email in attendees:
      assert email in HTTPretty.last_request.body.decode('utf-8')

  @raises(ValueError)
  def test_resources_must_have_an_email_address(self):

    HTTPretty.register_uri(HTTPretty.POST, FAKE_EXCHANGE_URL,
                             body=CREATE_ITEM_RESPONSE.encode('utf-8'),
                             content_type='text/xml; charset=utf-8')

    attendees = [PERSON_WITH_NO_EMAIL_ADDRESS]

    self.event.attendees = attendees
    self.event.create()

  @httprettified
  def test_resources(self):

    HTTPretty.register_uri(HTTPretty.POST, FAKE_EXCHANGE_URL,
                             body=CREATE_ITEM_RESPONSE.encode('utf-8'),
                             content_type='text/xml; charset=utf-8')


    self.event.resources = [RESOURCE.email]
    self.event.create()

    assert RESOURCE.email in HTTPretty.last_request.body.decode('utf-8')


