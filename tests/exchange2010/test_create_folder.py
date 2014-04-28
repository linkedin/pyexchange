"""
(c) 2013 LinkedIn Corp. All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License");?you may not use this file except in compliance with the License. You may obtain a copy of the License at  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software?distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
from httpretty import HTTPretty, httprettified
from nose.tools import eq_, raises
from pyexchange import Exchange2010Service

from pyexchange.connection import ExchangeNTLMAuthConnection
from pyexchange.exceptions import *

from .fixtures import *


class Test_PopulatingANewFolder():
  """ Tests all the attribute setting works when creating a new folder """
  folder = None

  @classmethod
  def setUpAll(cls):

    cls.folder = Exchange2010Service(
      connection=ExchangeNTLMAuthConnection(
        url=FAKE_EXCHANGE_URL,
        username=FAKE_EXCHANGE_USERNAME,
        password=FAKE_EXCHANGE_PASSWORD
      )
    ).folder()

  def test_canary(self):
    folder = self.folder.new_folder()
    assert folder is not None

  def test_folders_created_dont_have_an_id(self):
    folder = self.folder.new_folder()
    eq_(folder.id, None)

  def test_folder_has_display_name(self):
    folder = self.folder.new_folder(display_name=u'Conference Room')
    eq_(folder.display_name, u'Conference Room')

  def test_folder_has_default_folder_type(self):
    folder = self.folder.new_folder()
    eq_(folder.folder_type, u'Folder')

  def test_folder_has_calendar_folder_type(self):
    folder = self.folder.new_folder(folder_type=u'CalendarFolder')
    eq_(folder.folder_type, u'CalendarFolder')


class Test_CreatingANewFolder(object):
  service = None
  folder = None

  @classmethod
  def setUpAll(cls):
    cls.service = Exchange2010Service(
      connection=ExchangeNTLMAuthConnection(
        url=FAKE_EXCHANGE_URL,
        username=FAKE_EXCHANGE_USERNAME,
        password=FAKE_EXCHANGE_PASSWORD,
      )
    )

  def setUp(self):
    self.folder = self.service.folder().new_folder()

  @raises(AttributeError)
  def test_folders_must_have_a_display_name(self):
    self.parent_id = u'AQASAGFyMTY2AUB0eHN0YXRlLmVkdQAuAAADXToP9jZJ50ix6mBloAoUtQEAIXy9HV1hQUKHHMQm+PlY6QINNPfbUQAAAA=='
    self.folder.create()

  @raises(ValueError)
  def test_folders_must_have_a_parent_id(self):
    self.folder.display_name = u'Conference Room'
    self.parent_id = None
    self.folder.create()

  @raises(TypeError)
  def cant_delete_an_uncreated_folder(self):
    self.folder.delete()

  @httprettified
  def test_can_set_display_name(self):

    HTTPretty.register_uri(
      HTTPretty.POST,
      FAKE_EXCHANGE_URL,
      body=CREATE_FOLDER_RESPONSE.encode('utf-8'),
      content_type='text/xml; charset=utf-8',
    )

    self.folder.display_name = TEST_FOLDER.display_name
    self.folder.parent_id = TEST_FOLDER.parent_id
    self.folder.create()

    assert TEST_FOLDER.display_name in HTTPretty.last_request.body.decode('utf-8')

  @httprettified
  def test_can_set_parent_id(self):

    HTTPretty.register_uri(
      HTTPretty.POST,
      FAKE_EXCHANGE_URL,
      body=CREATE_FOLDER_RESPONSE.encode('utf-8'),
      content_type='text/xml; charset=utf-8',
    )

    self.folder.display_name = TEST_FOLDER.display_name
    self.folder.parent_id = TEST_FOLDER.parent_id
    self.folder.create()

    assert TEST_FOLDER.display_name in HTTPretty.last_request.body.decode('utf-8')

  @httprettified
  def test_can_set_folder_type(self):

    HTTPretty.register_uri(
      HTTPretty.POST,
      FAKE_EXCHANGE_URL,
      body=CREATE_FOLDER_RESPONSE.encode('utf-8'),
      content_type='text/xml; charset=utf-8',
    )

    self.folder.display_name = TEST_FOLDER.display_name
    self.folder.parent_id = TEST_FOLDER.parent_id
    self.folder.folder_type = TEST_FOLDER.folder_type
    self.folder.create()

    assert TEST_FOLDER.folder_type in HTTPretty.last_request.body.decode('utf-8')

  @httprettified
  def test_can_create(self):

    HTTPretty.register_uri(
      HTTPretty.POST,
      FAKE_EXCHANGE_URL,
      body=CREATE_FOLDER_RESPONSE.encode('utf-8'),
      content_type='text/html; charset=utf-8',
    )

    self.folder.display_name = TEST_FOLDER.display_name
    self.folder.parent_id = TEST_FOLDER.parent_id
    self.folder.folder_type = TEST_FOLDER.folder_type
    self.folder.create()

    eq_(self.folder.id, TEST_FOLDER.id)
