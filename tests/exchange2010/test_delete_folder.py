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


class Test_FolderDeletion(unittest.TestCase):
  folder = None

  @classmethod
  def setUpClass(cls):
    cls.service = Exchange2010Service(
      connection=ExchangeNTLMAuthConnection(
        url=FAKE_EXCHANGE_URL,
        username=FAKE_EXCHANGE_USERNAME,
        password=FAKE_EXCHANGE_PASSWORD,
      )
    )

    cls.get_change_key_response = httpretty.Response(
      body=GET_FOLDER_RESPONSE.encode('utf-8'),
      status=200,
      content_type='text/xml; charset=utf-8'
    )
    cls.delete_folder_response = httpretty.Response(
      body=DELETE_FOLDER_RESPONSE.encode('utf-8'),
      status=200,
      content_type='text/xml; charset=utf-8'
    )

  @httpretty.activate
  def setUp(self):

    httpretty.register_uri(
      httpretty.POST,
      FAKE_EXCHANGE_URL,
      body=GET_FOLDER_RESPONSE.encode('utf-8'),
      content_type='text/xml; charset=utf-8',
    )

    self.folder = self.service.folder().get_folder(id=TEST_FOLDER.id)

  @httpretty.activate
  def test_can_delete_folder(self):
    httpretty.register_uri(
      httpretty.POST,
      FAKE_EXCHANGE_URL,
      responses=[
        self.get_change_key_response,
        self.delete_folder_response,
      ]
    )

    response = self.folder.delete()
    assert response is None

  @httpretty.activate
  def test_cant_delete_a_uncreated_folder(self):
    httpretty.register_uri(
      httpretty.POST,
      FAKE_EXCHANGE_URL,
      responses=[
        self.get_change_key_response,
        self.delete_folder_response,
      ]
    )
    unsaved_folder = self.service.folder().new_folder()

    with raises(TypeError):
      unsaved_folder.delete()  # bzzt - can't do this
