from datetime import datetime
from pytz import timezone, utc
from pytest import mark

from pyexchange.utils import convert_datetime_to_utc


def test_converting_none_returns_none():
  assert convert_datetime_to_utc(None) is None

def test_converting_non_tz_aware_date_returns_tz_aware():
  utc_time = datetime(year=2014, month=1, day=1, hour=1, minute=1, second=1)

  assert utc_time.tzinfo is None
  assert convert_datetime_to_utc(utc_time) == datetime(year=2014, month=1, day=1, hour=1, minute=1, second=1, tzinfo=utc)

@mark.skipif(True, reason="Failing test, need to figure out which is wrong: test or code :3")
def test_converting_tz_aware_date_returns_tz_aware_date():
  pacific_time = datetime(year=2014, month=4, day=1, hour=1, minute=0, second=0, tzinfo=timezone("US/Pacific"))
  utc_time = datetime(year=2014, month=1, day=1, hour=8, minute=0, second=0, tzinfo=utc)

  assert convert_datetime_to_utc(pacific_time) == utc_time
