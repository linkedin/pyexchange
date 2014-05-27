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


class Test_ParseFolderResponseData(object):
  folder = None

  @classmethod
  def setUpAll(cls):

    @httpretty.activate  # this decorator doesn't play nice with @classmethod
    def fake_folder_request():

      service = Exchange2010Service(
        connection=ExchangeNTLMAuthConnection(
          url=FAKE_EXCHANGE_URL,
          username=FAKE_EXCHANGE_USERNAME,
          password=FAKE_EXCHANGE_PASSWORD,
        )
      )

      httpretty.register_uri(
        httpretty.POST,
        FAKE_EXCHANGE_URL,
        body=GET_FOLDER_RESPONSE.encode('utf-8'),
        content_type='text/xml; charset=utf-8',
      )

      return service.folder().get_folder(id=TEST_FOLDER.id)

    cls.folder = fake_folder_request()

  def test_canary(self):
    assert self.folder is not None

  def test_folder_id_was_not_changed(self):
    eq_(self.folder.id, TEST_FOLDER.id)

  def test_folder_has_a_name(self):
    eq_(self.folder.display_name, TEST_FOLDER.display_name)

  def test_folder_has_a_parent(self):
    eq_(self.folder.parent_id, TEST_FOLDER.parent_id)

  def test_folder_type(self):
    eq_(self.folder.folder_type, TEST_FOLDER.folder_type)


class Test_FailingToGetFolders():

  service = None

  @classmethod
  def setUpAll(cls):

    cls.service = Exchange2010Service(
      connection=ExchangeNTLMAuthConnection(
        url=FAKE_EXCHANGE_URL,
        username=FAKE_EXCHANGE_USERNAME,
        password=FAKE_EXCHANGE_PASSWORD
      )
    )

  @raises(ExchangeItemNotFoundException)
  @httpretty.activate
  def test_requesting_an_folder_id_that_doest_exist_throws_exception(self):

    httpretty.register_uri(
      httpretty.POST, FAKE_EXCHANGE_URL,
      body=FOLDER_DOES_NOT_EXIST.encode('utf-8'),
      content_type='text/xml; charset=utf-8',
    )

    self.service.folder().get_folder(id=TEST_FOLDER.id)

  @raises(FailedExchangeException)
  @httpretty.activate
  def test_requesting_an_folder_and_getting_a_500_response_throws_exception(self):

    httpretty.register_uri(
      httpretty.POST,
      FAKE_EXCHANGE_URL,
      body=u"",
      status=500,
      content_type='text/xml; charset=utf-8',
    )

    self.service.folder().get_folder(id=TEST_FOLDER.id)
