"""
(c) 2013 LinkedIn Corp. All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License");?you may not use this file except in compliance with the License. You may obtain a copy of the License at  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software?distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
from httpretty import HTTPretty, httprettified
from nose.tools import raises
from pyexchange import Exchange2010Service

from pyexchange.connection import ExchangeNTLMAuthConnection

from .fixtures import *

class Test_UpdatingAnEvent(object):
  service = None
  event = None

  @classmethod
  def setUpAll(cls):
    cls.service =  Exchange2010Service(connection=ExchangeNTLMAuthConnection(url=FAKE_EXCHANGE_URL, username=FAKE_EXCHANGE_USERNAME, password=FAKE_EXCHANGE_PASSWORD))
    cls.get_change_key_response = HTTPretty.Response(body=GET_ITEM_RESPONSE_ID_ONLY.encode('utf-8'), status=200, content_type='text/xml; charset=utf-8')
    cls.update_event_response   = HTTPretty.Response(body=UPDATE_ITEM_RESPONSE.encode('utf-8'), status=200, content_type='text/xml; charset=utf-8')

  @httprettified
  def setUp(self):

    HTTPretty.register_uri(HTTPretty.POST, FAKE_EXCHANGE_URL,
                                 body=GET_ITEM_RESPONSE.encode('utf-8'),
                                 content_type='text/xml; charset=utf-8')

    self.event = self.service.calendar().get_event(id=TEST_EVENT.id)


  @raises(ValueError)
  def test_events_must_have_a_start_date(self):
    self.event.start = None
    self.event.update()

  @raises(ValueError)
  def test_events_must_have_an_end_date(self):
    self.event.start = None
    self.event.update()

  @raises(ValueError)
  def test_event_end_date_must_come_after_start_date(self):
    self.event.start, self.event.end = self.event.end, self.event.start
    self.event.update()

  @httprettified
  def test_can_set_subject(self):

    HTTPretty.register_uri(HTTPretty.POST, FAKE_EXCHANGE_URL,
                           responses=[
                               self.get_change_key_response,
                               self.update_event_response,
                            ])

    self.event.subject = TEST_EVENT_UPDATED.subject
    self.event.update()

    assert TEST_EVENT_UPDATED.subject  in HTTPretty.last_request.body.decode('utf-8')

  @httprettified
  def test_can_set_location(self):

    HTTPretty.register_uri(HTTPretty.POST, FAKE_EXCHANGE_URL,
                           responses=[
                               self.get_change_key_response,
                               self.update_event_response,
                            ])


    self.event.location = TEST_EVENT_UPDATED.location
    self.event.update()

    assert TEST_EVENT_UPDATED.location in HTTPretty.last_request.body.decode('utf-8')

  @httprettified
  def test_can_set_html_body(self):

    HTTPretty.register_uri(HTTPretty.POST, FAKE_EXCHANGE_URL,
                           responses=[
                               self.get_change_key_response,
                               self.update_event_response,
                            ])

    self.event.html_body = TEST_EVENT_UPDATED.body
    self.event.update()

    assert TEST_EVENT_UPDATED.body in HTTPretty.last_request.body.decode('utf-8')

  @httprettified
  def test_can_set_text_body(self):

    HTTPretty.register_uri(HTTPretty.POST, FAKE_EXCHANGE_URL,
                           responses=[
                               self.get_change_key_response,
                               self.update_event_response,
                            ])


    self.event.text_body = TEST_EVENT_UPDATED.body
    self.event.update()

    assert TEST_EVENT_UPDATED.body in HTTPretty.last_request.body.decode('utf-8')

  @httprettified
  def test_can_set_start_time(self):

    HTTPretty.register_uri(HTTPretty.POST, FAKE_EXCHANGE_URL,
                           responses=[
                               self.get_change_key_response,
                               self.update_event_response,
                            ])


    self.event.start = TEST_EVENT_UPDATED.start
    self.event.update()

    assert TEST_EVENT_UPDATED.start.strftime(EXCHANGE_DATE_FORMAT) in HTTPretty.last_request.body.decode('utf-8')

  @httprettified
  def test_can_set_end_time(self):

    HTTPretty.register_uri(HTTPretty.POST, FAKE_EXCHANGE_URL,
                           responses=[
                               self.get_change_key_response,
                               self.update_event_response,
                            ])
    self.event.end = TEST_EVENT_UPDATED.end
    self.event.update()

    assert TEST_EVENT_UPDATED.end.strftime(EXCHANGE_DATE_FORMAT) in HTTPretty.last_request.body.decode('utf-8')

  @httprettified
  def test_can_set_attendees(self):

    HTTPretty.register_uri(HTTPretty.POST, FAKE_EXCHANGE_URL,
                           responses=[
                               self.get_change_key_response,
                               self.update_event_response,
                            ])

    attendees = [SIR_NOT_APPEARING_IN_THIS_FILM.email, PERSON_REQUIRED_ACCEPTED]

    self.event.attendees = attendees
    self.event.update()

    assert SIR_NOT_APPEARING_IN_THIS_FILM.email in HTTPretty.last_request.body.decode('utf-8')
    assert PERSON_REQUIRED_ACCEPTED.email in HTTPretty.last_request.body.decode('utf-8')

  @httprettified
  def test_can_set_required_attendees(self):
    HTTPretty.register_uri(HTTPretty.POST, FAKE_EXCHANGE_URL,
                           responses=[
                               self.get_change_key_response,
                               self.update_event_response,
                            ])

    required_attendees = [SIR_NOT_APPEARING_IN_THIS_FILM.email, PERSON_REQUIRED_ACCEPTED]

    self.event.required_attendees = required_attendees
    self.event.update()

    assert SIR_NOT_APPEARING_IN_THIS_FILM.email in HTTPretty.last_request.body.decode('utf-8')
    assert PERSON_REQUIRED_ACCEPTED.email in HTTPretty.last_request.body.decode('utf-8')
    assert PERSON_REQUIRED_DECLINED.email not in HTTPretty.last_request.body.decode('utf-8')
    assert PERSON_OPTIONAL_ACCEPTED.email in HTTPretty.last_request.body.decode('utf-8')

  @httprettified
  def test_can_set_optional_attendees(self):
    HTTPretty.register_uri(HTTPretty.POST, FAKE_EXCHANGE_URL,
                           responses=[
                               self.get_change_key_response,
                               self.update_event_response,
                            ])

    optional_attendees = [SIR_NOT_APPEARING_IN_THIS_FILM.email, PERSON_OPTIONAL_ACCEPTED]

    self.event.optional_attendees = optional_attendees
    self.event.update()

    assert SIR_NOT_APPEARING_IN_THIS_FILM.email in HTTPretty.last_request.body.decode('utf-8')
    assert PERSON_OPTIONAL_ACCEPTED.email in HTTPretty.last_request.body.decode('utf-8')
    assert PERSON_OPTIONAL_DECLINED.email not in HTTPretty.last_request.body.decode('utf-8')
    assert PERSON_REQUIRED_ACCEPTED.email in HTTPretty.last_request.body.decode('utf-8')

  @raises(ValueError)
  def test_attendees_must_have_an_email_address(self):
    self.event.attendees = [PERSON_REQUIRED_ACCEPTED.email, None] # list of email addresses

  @raises(ValueError)
  def test_attendee_objects_must_have_an_email_address(self):
    self.event.attendees = [PERSON_WITH_NO_EMAIL_ADDRESS]

  def test_can_add_attendees_by_email_address(self):
    attendee_count = len(self.event.attendees)
    self.event.add_attendees([SIR_NOT_APPEARING_IN_THIS_FILM.email, SIR_ROBIN.email ])

    assert len(self.event.attendees) == attendee_count + 2
    assert SIR_NOT_APPEARING_IN_THIS_FILM.email in [attendee.email for attendee in self.event.attendees]
    assert SIR_ROBIN.email in [attendee.email for attendee in self.event.attendees]


  def test_can_add_attendees_by_object(self):
    attendee_count = len(self.event.attendees)
    self.event.add_attendees([SIR_NOT_APPEARING_IN_THIS_FILM, SIR_ROBIN])

    assert len(self.event.attendees) == attendee_count + 2
    assert SIR_NOT_APPEARING_IN_THIS_FILM.email in [attendee.email for attendee in self.event.attendees]
    assert SIR_ROBIN.email in [attendee.email for attendee in self.event.attendees]

  def test_can_delete_attendees_by_email_address(self):
    attendee_count = len(self.event.attendees)
    self.event.remove_attendees(PERSON_REQUIRED_DECLINED.email)

    assert len(self.event.attendees) == attendee_count - 1
    assert PERSON_REQUIRED_DECLINED.email not in [attendee.email for attendee in self.event.attendees]

  def test_can_delete_attendees_by_object(self):
    attendee_count = len(self.event.attendees)
    self.event.remove_attendees(PERSON_REQUIRED_DECLINED)

    assert len(self.event.attendees) == attendee_count - 1
    assert PERSON_REQUIRED_DECLINED.email not in [attendee.email for attendee in self.event.attendees]

  def test_cant_add_an_attendee_twice(self):
    attendee_count = len(self.event.attendees)

    assert PERSON_REQUIRED_DECLINED.email in [attendee.email for attendee in self.event.attendees]
    self.event.add_resources(PERSON_REQUIRED_DECLINED)

    assert len(self.event.attendees) == attendee_count
    assert PERSON_REQUIRED_DECLINED.email in [attendee.email for attendee in self.event.attendees]

  @httprettified
  def test_can_remove_all_attendees(self):
    HTTPretty.register_uri(HTTPretty.POST, FAKE_EXCHANGE_URL,
                         responses=[
                             self.get_change_key_response,
                             self.update_event_response,
                          ])


    self.event.attendees = None
    self.event.update()

    assert RESOURCE.email not in HTTPretty.last_request.body.decode('utf-8')


  @httprettified
  def test_can_change_resources(self):

    HTTPretty.register_uri(HTTPretty.POST, FAKE_EXCHANGE_URL,
                           responses=[
                               self.get_change_key_response,
                               self.update_event_response,
                            ])


    self.event.resources = [UPDATED_RESOURCE.email]
    self.event.update()

    assert UPDATED_RESOURCE.email in HTTPretty.last_request.body.decode('utf-8')

  @httprettified
  def test_can_remove_all_resources(self):
    HTTPretty.register_uri(HTTPretty.POST, FAKE_EXCHANGE_URL,
                         responses=[
                             self.get_change_key_response,
                             self.update_event_response,
                          ])


    self.event.resources = None
    self.event.update()

    assert RESOURCE.email not in HTTPretty.last_request.body.decode('utf-8')

  def test_can_add_resources_by_email_address(self):
    resource_count = len(self.event.resources)

    self.event.add_resources(UPDATED_RESOURCE.email)

    assert len(self.event.resources) == resource_count + 1
    assert UPDATED_RESOURCE.email in [resource.email for resource in self.event.resources]

  def test_can_add_resources_by_object(self):
    resource_count = len(self.event.resources)
    self.event.add_resources(UPDATED_RESOURCE)

    assert len(self.event.resources) == resource_count + 1
    assert UPDATED_RESOURCE.email in [resource.email for resource in self.event.resources]

  def test_can_delete_resources_by_email_address(self):
    resource_count = len(self.event.resources)

    self.event.remove_resources(RESOURCE.email)

    assert len(self.event.resources) == resource_count - 1
    assert RESOURCE.email not in [resource.email for resource in self.event.resources]

  def test_can_delete_resources_by_object(self):
    resource_count = len(self.event.resources)

    self.event.remove_resources(RESOURCE)

    assert len(self.event.resources) == resource_count - 1
    assert RESOURCE.email not in [resource.email for resource in self.event.resources]

  @raises(ValueError)
  def test_resources_must_have_an_email_address(self):
    self.event.resources = [RESOURCE.email, None]


  @raises(ValueError)
  def test_resource_objects_must_have_an_email_address(self):
    self.event.resources = [RESOURCE_WITH_NO_EMAIL_ADDRESS]

  @httprettified
  def test_changes_are_normally_sent_to_everybody(self):

    HTTPretty.register_uri(HTTPretty.POST, FAKE_EXCHANGE_URL,
                           responses=[
                               self.get_change_key_response,
                               self.update_event_response,
                            ])


    self.event.resources = [UPDATED_RESOURCE.email]
    self.event.update()
    assert u"SendToAllAndSaveCopy" in HTTPretty.last_request.body.decode('utf-8')

  @httprettified
  def test_changes_are_normally_sent_to_everybody_unless_the_flag_is_specified(self):

    HTTPretty.register_uri(HTTPretty.POST, FAKE_EXCHANGE_URL,
                           responses=[
                               self.get_change_key_response,
                               self.update_event_response,
                            ])


    self.event.resources = [UPDATED_RESOURCE.email]
    self.event.update(send_only_to_changed_attendees=True)

    assert u"SendToChangedAndSaveCopy" in HTTPretty.last_request.body.decode('utf-8')

  @httprettified
  def test_changes_are_sent_to_nobody(self):

    HTTPretty.register_uri(HTTPretty.POST, FAKE_EXCHANGE_URL,
                           responses=[
                               self.get_change_key_response,
                               self.update_event_response,
                            ])


    self.event.resources = [UPDATED_RESOURCE.email]
    self.event.update(calendar_item_update_operation_type='SendToNone')

    assert u"SendToNone" in HTTPretty.last_request.body.decode('utf-8')

  @httprettified
  def test_changes_are_sent_only_to_all(self):

    HTTPretty.register_uri(HTTPretty.POST, FAKE_EXCHANGE_URL,
                           responses=[
                               self.get_change_key_response,
                               self.update_event_response,
                            ])


    self.event.resources = [UPDATED_RESOURCE.email]
    self.event.update(calendar_item_update_operation_type='SendOnlyToAll')

    assert u"SendOnlyToAll" in HTTPretty.last_request.body.decode('utf-8')

  @httprettified
  def test_changes_are_sent_only_to_changed(self):

    HTTPretty.register_uri(HTTPretty.POST, FAKE_EXCHANGE_URL,
                           responses=[
                               self.get_change_key_response,
                               self.update_event_response,
                            ])


    self.event.resources = [UPDATED_RESOURCE.email]
    self.event.update(calendar_item_update_operation_type='SendOnlyToChanged')

    assert u"SendOnlyToChanged" in HTTPretty.last_request.body.decode('utf-8')

  @httprettified
  def test_changes_are_sent_to_all_and_save_copy(self):

    HTTPretty.register_uri(HTTPretty.POST, FAKE_EXCHANGE_URL,
                           responses=[
                               self.get_change_key_response,
                               self.update_event_response,
                            ])


    self.event.resources = [UPDATED_RESOURCE.email]
    self.event.update(calendar_item_update_operation_type='SendToAllAndSaveCopy')

    assert u"SendToAllAndSaveCopy" in HTTPretty.last_request.body.decode('utf-8')

  @httprettified
  def test_changes_are_sent_to_changed_and_save_copy(self):

    HTTPretty.register_uri(HTTPretty.POST, FAKE_EXCHANGE_URL,
                           responses=[
                               self.get_change_key_response,
                               self.update_event_response,
                            ])


    self.event.resources = [UPDATED_RESOURCE.email]
    self.event.update(calendar_item_update_operation_type='SendToChangedAndSaveCopy')

    assert u"SendToChangedAndSaveCopy" in HTTPretty.last_request.body.decode('utf-8')

  @raises(ValueError)
  def test_wrong_update_operation(self):

    HTTPretty.register_uri(HTTPretty.POST, FAKE_EXCHANGE_URL,
                           responses=[
                               self.get_change_key_response,
                               self.update_event_response,
                            ])


    self.event.resources = [UPDATED_RESOURCE.email]
    self.event.update(calendar_item_update_operation_type='SendToTheWholeWorld')

    assert u"SendToTheWholeWorld" in HTTPretty.last_request.body.decode('utf-8')
