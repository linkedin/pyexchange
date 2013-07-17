"""
(c) 2013 LinkedIn Corp. All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License");?you may not use this file except in compliance with the License. You may obtain a copy of the License at  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software?distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
from httpretty import HTTPretty, httprettified
from nose.tools import raises
from pyexchange import Exchange2010Service
from pyexchange.connection import ExchangeNTLMAuthConnection
from pyexchange.exceptions import *

from .fixtures import *
from .. import wip

class Test_EventActions(object):
  event = None

  @classmethod
  def setUpAll(cls):
    cls.service = Exchange2010Service(connection=ExchangeNTLMAuthConnection(url=FAKE_EXCHANGE_URL, username=FAKE_EXCHANGE_USERNAME, password=FAKE_EXCHANGE_PASSWORD))
    cls.get_change_key_response = HTTPretty.Response(body=GET_ITEM_RESPONSE_ID_ONLY.encode('utf-8'), status=200, content_type='text/xml; charset=utf-8')
    cls.update_event_response   = HTTPretty.Response(body=UPDATE_ITEM_RESPONSE.encode('utf-8'), status=200, content_type='text/xml; charset=utf-8')


  @httprettified
  def setUp(self):
    HTTPretty.register_uri(HTTPretty.POST, FAKE_EXCHANGE_URL,
                                 body=GET_ITEM_RESPONSE.encode('utf-8'),
                                 content_type='text/xml; charset=utf-8')

    self.event = self.service.calendar().get_event(id=TEST_EVENT.id)


  @httprettified
  def test_resend_invites(self):
    HTTPretty.register_uri(HTTPretty.POST, FAKE_EXCHANGE_URL,
                           responses=[
                               self.get_change_key_response,
                               self.update_event_response,
                            ])
    self.event.resend_invitations()

    assert TEST_EVENT.change_key in HTTPretty.last_request.body.decode('utf-8')
    assert TEST_EVENT.subject not in HTTPretty.last_request.body.decode('utf-8')


  @raises(ValueError)
  @httprettified
  def test_cant_resend_invites_on_a_modified_event(self):
    HTTPretty.register_uri(HTTPretty.POST, FAKE_EXCHANGE_URL,
                           responses=[
                               self.get_change_key_response,
                               self.update_event_response,
                            ])

    self.event.subject = u'New event thing'
    self.event.resend_invitations()
