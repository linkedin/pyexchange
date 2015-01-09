import sys

IS_PYTHON3 = sys.version_info >= (3, 0)

if IS_PYTHON3:
  BASESTRING_TYPES = str
else:
  BASESTRING_TYPES = (str, unicode)

def _unicode(item):
  if IS_PYTHON3:
    return str(item)
  else:
    return unicode(item)