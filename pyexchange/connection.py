"""
(c) 2013 LinkedIn Corp. All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License");?you may not use this file except in compliance with the License. You may obtain a copy of the License at  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software?distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
import logging
import sys
from ntlm import HTTPNtlmAuthHandler

try:
  import urllib2
except ImportError:  # Python 3
  import urllib.request as urllib2

try:
  from httplib import HTTPException
except ImportError:  # Python 3
  from http.client import HTTPException

from .exceptions import FailedExchangeException

log = logging.getLogger('pyexchange')


class ExchangeBaseConnection(object):
  """ Base class for Exchange connections."""

  def send(self, body, headers=None, retries=2, timeout=30, encoding="utf-8"):
    raise NotImplementedError


class ExchangeNTLMAuthConnection(ExchangeBaseConnection):
  """ Connection to Exchange that uses NTLM authentication """

  def __init__(self, url, username, password, **kwargs):
    self.url = url
    self.username = username
    self.password = password

    self.handler = None
    self.opener = None
    self.password_manager = None

  def build_password_manager(self):
    if self.password_manager:
      return self.password_manager

    log.debug(u'Constructing password manager')

    self.password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
    self.password_manager.add_password(None, self.url, self.username, self.password)

    return self.password_manager

  def build_handler(self):
    if self.handler:
      return self.handler

    log.debug(u'Constructing handler')

    self.password_manager = self.build_password_manager()
    self.handler = HTTPNtlmAuthHandler.HTTPNtlmAuthHandler(self.password_manager)

    return self.handler

  def build_opener(self):
    if self.opener:
      return self.opener

    log.debug(u'Constructing opener')

    self.handler = self.build_handler()
    self.opener = urllib2.build_opener(self.handler)

    return self.opener

  def send(self, body, headers=None, retries=2, timeout=30, encoding=u"utf-8"):
    if not self.opener:
      self.opener = self.build_opener()

    # lxml tostring returns str in Python 2, and bytes in python 3
    # if XML is actually unicode, urllib2 will barf.
    # Oddly enough this only seems to be a problem in 2.7. 2.6 doesn't seem to care.
    if sys.version_info < (3, 0):
      if isinstance(body, unicode):
        body = body.encode(encoding)
    else:
      if isinstance(body, str):
        body = body.encode(encoding)

    request = urllib2.Request(self.url, body)

    if headers:
      for header in headers:
        log.debug(u'Adding header: {name} - {value}'.format(name=header[0], value=header[1]))
        request.add_header(header[0], header[1])

    error = None
    for retry in range(retries + 1):
      log.info(u'Connection attempt #{0} of {1}'.format(retry + 1, retries))
      try:
        # retrieve the result
        log.info(u'Sending request to url: {0}'.format(request.get_full_url()))
        try:
          response = self.opener.open(request, timeout=timeout)

        except urllib2.HTTPError as err:
          # Called for 500 errors
          raise FailedExchangeException(u'Unable to connect to Exchange: %s' % err)

        response_code = response.getcode()
        body = response.read().decode(encoding)

        log.info(u'Got response: {code}'.format(code=response_code))
        log.debug(u'Got response headers: {headers}'.format(headers=response.info()))
        log.debug(u'Got body: {body}'.format(body=body))

        return body
      except HTTPException as err:
        log.error(u'Caught err, retrying: {err}'.format(err=err))
        error = err

    # All retries used up, re-throw the exception.
    raise error
