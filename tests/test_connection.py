"""
(c) 2013 LinkedIn Corp. All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License");?you may not use this file except in compliance with the License. You may obtain a copy of the License at  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software?distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
import httpretty
import unittest
from pytest import raises
from pyexchange.connection import ExchangeNTLMAuthConnection
from pyexchange.exceptions import *


from .fixtures import *


class Test_ExchangeNTLMAuthConnection(unittest.TestCase):

  service = None

  @classmethod
  def setUpClass(cls):

    cls.connection=ExchangeNTLMAuthConnection(url=FAKE_EXCHANGE_URL,
                                              username=FAKE_EXCHANGE_USERNAME,
                                              password=FAKE_EXCHANGE_PASSWORD)


  @httpretty.activate
  def test_requesting_an_event_id_that_doest_exist_throws_error(self):

    httpretty.register_uri(httpretty.POST, FAKE_EXCHANGE_URL,
                           status=401,
                           body="", )

    with raises(FailedExchangeException):
      self.connection.send(b'yo')

