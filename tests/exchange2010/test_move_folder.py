"""
(c) 2013 LinkedIn Corp. All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License");?you may not use this file except in compliance with the License. You may obtain a copy of the License at  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software?distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
from httpretty import HTTPretty, httprettified
from nose.tools import eq_, raises
from pyexchange import Exchange2010Service

from pyexchange.connection import ExchangeNTLMAuthConnection

from .fixtures import *


class Test_MovingAFolder(object):
  service = None
  folder = None

  @classmethod
  def setUpAll(self):
    self.service = Exchange2010Service(
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
      body=GET_FOLDER_RESPONSE.encode('utf-8'),
      content_type='text/xml; charset=utf-8'
    )

    self.folder = self.service.folder().get_folder(id=TEST_FOLDER.id)

  @raises(TypeError)
  def test_move_empty_folder_id(self):

    self.folder.move_to(None)

  @raises(TypeError)
  def test_move_bad_folder_id_type(self):

    self.folder.move_to(self.folder)

  @httprettified
  def test_move(self):

    HTTPretty.register_uri(
      HTTPretty.POST,
      FAKE_EXCHANGE_URL,
      body=MOVE_FOLDER_RESPONSE.encode('utf-8'),
      content_type='text/xml; charset=utf-8'
    )

    self.folder.move_to('AABBCCDDEEFFGG==')
    eq_(self.folder.parent_id, 'AABBCCDDEEFFGG==')
