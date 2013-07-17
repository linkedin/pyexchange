"""
(c) 2013 LinkedIn Corp. All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License");?you may not use this file except in compliance with the License. You may obtain a copy of the License at  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software?distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
import logging
from .exchange2010 import Exchange2010Service  # noqa
from .connection import ExchangeNTLMAuthConnection  # noqa

# Silence notification of no default logging handler
log = logging.getLogger("pyexchange")


class NullHandler(logging.Handler):
  def emit(self, record):
    pass

log.addHandler(NullHandler())
