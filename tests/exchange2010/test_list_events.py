
import unittest
from pytest import raises
from httpretty import HTTPretty, httprettified
from pyexchange import Exchange2010Service
from pyexchange.connection import ExchangeNTLMAuthConnection
from pyexchange.exceptions import *

from .fixtures import *


class Test_ParseEventListResponseData(unittest.TestCase):
    service = None
    event_list = None

    @classmethod
    def setUpClass(cls):
        cls.service = Exchange2010Service(
            connection=ExchangeNTLMAuthConnection(
                url=FAKE_EXCHANGE_URL,
                username=FAKE_EXCHANGE_USERNAME,
                password=FAKE_EXCHANGE_PASSWORD
            )
        )

    @httprettified
    def setUp(self):
        HTTPretty.register_uri(
            HTTPretty.POST, FAKE_EXCHANGE_URL,
            body=LIST_EVENTS_RESPONSE.encode('utf-8'),
            content_type='text/xml; charset=utf-8'
        )
        self.event_list = self.service.calendar().list_events(
            start=TEST_EVENT_LIST_START,
            end=TEST_EVENT_LIST_END
        )

    def test_canary(self):
        assert self.event_list is not None

    def test_dates_are_in_datetime_format(self):
        assert 'StartDate="%s"' % TEST_EVENT_LIST_START.strftime(EXCHANGE_DATETIME_FORMAT) in HTTPretty.last_request.body.decode('utf-8')
        assert 'EndDate="%s"' % TEST_EVENT_LIST_END.strftime(EXCHANGE_DATETIME_FORMAT) in HTTPretty.last_request.body.decode('utf-8')

    def test_event_count(self):
        assert self.event_list.count == 3

    def test_first_event_subject(self):
        assert self.event_list.events[0].subject == 'Event Subject 1'

    def test_second_event_subject(self):
        assert self.event_list.events[1].subject == 'Event Subject 2'


class Test_FailingToListEvents(unittest.TestCase):
    service = None

    @classmethod
    def setupClass(cls):

        cls.service = Exchange2010Service(
            connection=ExchangeNTLMAuthConnection(
                url=FAKE_EXCHANGE_URL,
                username=FAKE_EXCHANGE_USERNAME,
                password=FAKE_EXCHANGE_PASSWORD
            )
        )

    #@httpretty.activate
    def test_requesting_an_event_and_getting_a_500_response_throws_exception(self):
        pass
        # httpretty.register_uri(
        #     httpretty.POST, FAKE_EXCHANGE_URL,
        #     body=u"",
        #     status=500,
        #     content_type='text/xml; charset=utf-8'
        # )

        #with raises(FailedExchangeException):
        #    self.service.calendar().list_events(
        #        start=TEST_EVENT_LIST_START,
        #        end=TEST_EVENT_LIST_END
        #    )
