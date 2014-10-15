"""
(c) 2013 LinkedIn Corp. All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License");?you may not use this file except in compliance with the License. You may obtain a copy of the License at  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software?distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
import unittest
import httpretty
from pytest import raises
from pyexchange import Exchange2010Service
from pyexchange.connection import ExchangeNTLMAuthConnection

from .fixtures import *

class Test_EventDeletion(unittest.TestCase):
  event = None

  @classmethod
  def setUpClass(cls):
    cls.service =  Exchange2010Service(connection=ExchangeNTLMAuthConnection(url=FAKE_EXCHANGE_URL, username=FAKE_EXCHANGE_USERNAME, password=FAKE_EXCHANGE_PASSWORD))


    cls.get_change_key_response = httpretty.Response(body=GET_ITEM_RESPONSE_ID_ONLY.encode('utf-8'), status=200, content_type='text/xml; charset=utf-8')
    cls.delete_event_response   = httpretty.Response(body=DELETE_ITEM_RESPONSE.encode('utf-8'), status=200, content_type='text/xml; charset=utf-8')

  @httpretty.activate
  def setUp(self):

    httpretty.register_uri(httpretty.POST, FAKE_EXCHANGE_URL,
                                 body=GET_ITEM_RESPONSE.encode('utf-8'),
                                 content_type='text/xml; charset=utf-8')

    self.event = self.service.calendar().get_event(id=TEST_EVENT.id)


  @httpretty.activate
  def test_can_cancel_event(self):
    httpretty.register_uri(httpretty.POST, FAKE_EXCHANGE_URL,
                           responses=[
                               self.get_change_key_response,
                               self.delete_event_response,
                            ])

    response = self.event.cancel()
    assert response is None


  @httpretty.activate
  def test_cant_cancel_an_event_with_no_exchange_id(self):
    httpretty.register_uri(httpretty.POST, FAKE_EXCHANGE_URL,
                           responses=[
                               self.get_change_key_response,
                               self.delete_event_response,
                            ])
    unsaved_event = self.service.calendar().event()

    with raises(TypeError):
      unsaved_event.cancel() #bzzt - can't do this

