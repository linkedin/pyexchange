"""
(c) 2013 LinkedIn Corp. All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License");?you may not use this file except in compliance with the License. You may obtain a copy of the License at  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software?distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
from functools import wraps
from nose.plugins.attrib import attr
from nose.plugins.skip import SkipTest

"""
Got this from:

http://www.natpryce.com/articles/000788.html
https://gist.github.com/997195

"""


def fail(message):
  raise AssertionError(message)

def wip(f):
  """
  Use this as a decorator to mark tests that are "works in progress"
  """
  @wraps(f)
  def run_test(*args, **kwargs):
    try:
      f(*args, **kwargs)
    except Exception as e:
      raise SkipTest("WIP test failed: " + str(e))
    fail("test passed but marked as work in progress")

  return attr('wip')(run_test)