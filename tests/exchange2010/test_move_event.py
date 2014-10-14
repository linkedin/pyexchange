"""
(c) 2013 LinkedIn Corp. All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License");?you may not use this file except in compliance with the License. You may obtain a copy of the License at  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software?distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
import unittest
from httpretty import HTTPretty, httprettified
from pytest import raises
from pyexchange import Exchange2010Service

from pyexchange.connection import ExchangeNTLMAuthConnection

from .fixtures import *


class Test_MovingAnEvent(unittest.TestCase):
  service = None
  event = None

  @classmethod
  def setUpClass(cls):
    cls.service = Exchange2010Service(
      connection=ExchangeNTLMAuthConnection(
        url=FAKE_EXCHANGE_URL,
        username=FAKE_EXCHANGE_USERNAME,
        password=FAKE_EXCHANGE_PASSWORD,
      )
    )

  @httprettified
  def setUp(self):

    HTTPretty.register_uri(
      HTTPretty.POST,
      FAKE_EXCHANGE_URL,
      body=GET_ITEM_RESPONSE.encode('utf-8'),
      content_type='text/xml; charset=utf-8'
    )

    self.event = self.service.calendar().get_event(id=TEST_EVENT.id)

  def test_move_empty_folder_id(self):
    with raises(TypeError):
      self.event.move_to(None)

  def test_move_bad_folder_id_type(self):
    with raises(TypeError):
      self.event.move_to(self.event)

  @httprettified
  def test_move(self):

    HTTPretty.register_uri(
      HTTPretty.POST,
      FAKE_EXCHANGE_URL,
      body=MOVE_EVENT_RESPONSE.encode('utf-8'),
      content_type='text/xml; charset=utf-8'
    )

    self.event.move_to('AAAhKSe7AAA=')
    assert self.event.calendar_id == 'AAAhKSe7AAA='
    assert self.event.id == TEST_EVENT_MOVED.id
