"""
(c) 2013 LinkedIn Corp. All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License");?you may not use this file except in compliance with the License. You may obtain a copy of the License at  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software?distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
from pytz import utc


def convert_datetime_to_utc(datetime_to_convert):
  if datetime_to_convert is None:
    return None

  if datetime_to_convert.tzinfo:
    return datetime_to_convert.astimezone(utc)
  else:
    return utc.localize(datetime_to_convert)
