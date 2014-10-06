
import httpretty
from nose.tools import eq_, raises
from pyexchange import Exchange2010Service
from pyexchange.connection import ExchangeNTLMAuthConnection
from pyexchange.exceptions import *

from .fixtures import *


class Test_ParseEventListResponseData(object):
  list_event = None

  @classmethod
  def setUpAll(cls):

    @httpretty.activate  # this decorator doesn't play nice with @classmethod
    def fake_event_list_request():
      service = Exchange2010Service(
        connection=ExchangeNTLMAuthConnection(
          url=FAKE_EXCHANGE_URL,
          username=FAKE_EXCHANGE_USERNAME,
          password=FAKE_EXCHANGE_PASSWORD
        )
      )

      httpretty.register_uri(
        httpretty.POST, FAKE_EXCHANGE_URL,
        body=LIST_EVENTS_RESPONSE.encode('utf-8'),
        content_type='text/xml; charset=utf-8'
      )

      return service.calendar().list_events(
        start=TEST_EVENT_LIST_START,
        end=TEST_EVENT_LIST_END
      )

    cls.list_event = fake_event_list_request()

  def test_canary(self):
    assert self.list_event is not None

  def test_event_count(self):
    assert self.list_event.count == 3

  def test_first_event_subject(self):
    assert self.list_event.events[0].subject == 'Event Subject 1'

  def test_second_event_subject(self):
    assert self.list_event.events[1].subject == 'Event Subject 2'

class Test_FailingToListEvents():
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

  @raises(FailedExchangeException)
  @httpretty.activate
  def test_requesting_an_event_and_getting_a_500_response_throws_exception(self):

    httpretty.register_uri(
      httpretty.POST, FAKE_EXCHANGE_URL,
      body=u"",
      status=500,
      content_type='text/xml; charset=utf-8'
    )

    self.service.calendar().list_events(
      start=TEST_EVENT_LIST_START,
      end=TEST_EVENT_LIST_END
    )




