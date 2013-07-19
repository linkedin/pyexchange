"""
(c) 2013 LinkedIn Corp. All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License");?you may not use this file except in compliance with the License. You may obtain a copy of the License at  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software?distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""


class FailedExchangeException(Exception):
  """Raised when the Microsoft Exchange Server returns an error via SOAP for a request."""
  pass


class ExchangeInvalidIdMalformedException(FailedExchangeException):
  """Raised when we ask for an event key that doesn't exist."""
  pass


class ExchangeStaleChangeKeyException(FailedExchangeException):
  """Raised when a edit event fails due to a stale change key. Exchange requires a change token for all edit events,
  and they change every time an object is updated"""
  pass


class ExchangeItemNotFoundException(FailedExchangeException):
  """
  Raised when an item is not found on the Exchange server
  """
  pass
