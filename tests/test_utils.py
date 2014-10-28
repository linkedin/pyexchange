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

def test_converting_tz_aware_date_returns_tz_aware_date():
  # US/Pacific timezone is UTC-07:00 (In April we are in DST)
  # We use localize() because according to the pytz documentation, using the tzinfo
  # argument of the standard datetime constructors does not work for timezones with DST.
  pacific_time = timezone("US/Pacific").localize(datetime(year=2014, month=4, day=1, hour=1, minute=0, second=0))
  utc_time = utc.localize(datetime(year=2014, month=4, day=1, hour=8, minute=0, second=0))

  assert convert_datetime_to_utc(pacific_time) == utc_time
