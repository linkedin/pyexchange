class BaseExchangeFolderService(object):

  def __init__(self, service):
    self.service = service

  def get_folder(self, id, *args, **kwargs):
    raise NotImplementedError


class BaseExchangeFolder(object):

  _id = None
  _change_key = None
  _parent_id = None
  _parent_change_key = None
  _folder_type = u'Folder'

  _service = None

  _display_name = u''
  _child_folder_count = None
  _total_count = None

  _track_dirty_attributes = False
  _dirty_attributes = set()  # any attributes that have changed, and we need to update in Exchange

  FOLDER_TYPES = (u'Folder', u'CalendarFolder',)  # Need to add all types here

  def __init__(self, service, id=None, xml=None, **kwargs):
    self.service = service

    if xml is not None:
      self._init_from_xml(xml)
    elif id is None:
      self._update_properties(kwargs)
    else:
      self._init_from_service(id)

  def _init_from_xml(self, xml):
    raise NotImplementedError

  def _init_from_service(self, id):
    raise NotImplementedError

  def create(self):
    raise NotImplementedError

  def update(self):
    raise NotImplementedError

  def delete(self):
    raise NotImplementedError

  @property
  def id(self):
    """ **Read-only.** The internal id Exchange uses to refer to this event. """
    return self._id

  @property
  def change_key(self):
    """ **Read-only.** When you change an event, Exchange makes you pass a change key to prevent overwriting a previous version. """
    return self._change_key

  @property
  def parent_id(self):
    """ **Read-only.** The internal id Exchange uses to refer to this event. """
    return self._parent_id

  @parent_id.setter
  def parent_id(self, value):
    self._parent_id = value

  @property
  def folder_type(self):
    return self._folder_type

  @folder_type.setter
  def folder_type(self, value):
    if value in self.FOLDER_TYPES:
      self._folder_type = value

  def _update_properties(self, properties):
    self._track_dirty_attributes = False
    for key in properties:
      setattr(self, key, properties[key])
    self._track_dirty_attributes = True

  def __setattr__(self, key, value):
    """ Magically track public attributes, so we can track what we need to flush to the Exchange store """
    if self._track_dirty_attributes and not key.startswith(u"_"):
      self._dirty_attributes.add(key)

    object.__setattr__(self, key, value)

  def _reset_dirty_attributes(self):
    self._dirty_attributes = set()
