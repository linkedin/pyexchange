"""
(c) 2013 LinkedIn Corp. All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License");?you may not use this file except in compliance with the License. You may obtain a copy of the License at  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software?distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
from collections import namedtuple

try:
  import simplejson as json
except ImportError:
  import json

ExchangeEventOrganizer = namedtuple('ExchangeEventOrganizer', ['name', 'email'])
ExchangeEventAttendee = namedtuple('ExchangeEventAttendee', ['name', 'email', 'required'])
ExchangeEventResponse = namedtuple('ExchangeEventResponse', ['name', 'email', 'response', 'last_response', 'required'])


RESPONSE_ACCEPTED = u'Accept'
RESPONSE_DECLINED = u'Decline'
RESPONSE_TENTATIVE = u'Tentative'
RESPONSE_UNKNOWN = u'Unknown'

RESPONSES = [RESPONSE_ACCEPTED, RESPONSE_DECLINED, RESPONSE_TENTATIVE, RESPONSE_UNKNOWN]


class BaseExchangeCalendarService(object):

  def __init__(self, service, calendar_id):
    self.service = service
    self.calendar_id = calendar_id

  def event(self, id, *args, **kwargs):
    raise NotImplementedError

  def get_event(self, id):
    raise NotImplementedError

  def new_event(self, **properties):
    raise NotImplementedError


class BaseExchangeCalendarEvent(object):

  _id = None  # Exchange identifier for the event
  _change_key = None  # Exchange requires a second key when updating/deleting the event

  service = None
  calendar_id = None

  subject = u''
  start = None
  end = None
  location = None
  html_body = None
  text_body = None
  attachments = None
  organizer = None
  reminder_minutes_before_start = None
  is_all_day = None

  recurrence = None
  recurrence_end_date = None
  recurrence_days = None

  _type = None

  _attendees = {}  # people attending
  _resources = {}  # conference rooms attending

  _track_dirty_attributes = False
  _dirty_attributes = set()  # any attributes that have changed, and we need to update in Exchange

  # these attributes can be pickled, or output as JSON
  DATA_ATTRIBUTES = [
    u'_id', u'subject', u'start', u'end', u'location', u'html_body', u'text_body', u'organizer',
    u'_attendees', u'_resources', u'reminder_minutes_before_start', u'is_all_day',
    'recurrence', 'recurrence_interval', 'recurrence_days', 'recurrence_day',
  ]

  RECURRENCE_ATTRIBUTES = [
    'recurrence', 'recurrence_end_date', 'recurrence_days', 'recurrence_interval',
  ]

  WEEKLY_DAYS = [u'Sunday', u'Monday', u'Tuesday', u'Wednesday', u'Thursday', u'Friday', u'Saturday']

  def __init__(self, service, id=None, xml=None, calendar_id=u'calendar', **kwargs):
    self.service = service
    self.calendar_id = calendar_id

    if xml is not None:
      self._init_from_xml(xml)
    if id is None:
      self._update_properties(kwargs)
    else:
      self._init_from_service(id)

    self._track_dirty_attributes = True  # magically look for changed attributes

  def _init_from_xml(self, xml):
    """ Parse xml and create event from it.  Useful for creating events from a previous exchange response. """
    raise NotImplementedError

  def _init_from_service(self, id):
    """ Connect to the Exchange service and grab all the properties out of it. """
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
  def body(self):
    """ **Read-only.** Returns either the html_body or the text_body property, whichever is set. """
    return self.html_body or self.text_body or None

  @property
  def type(self):
    """ **Read-only.** This is an attribute pulled from an event in the exchange store. """
    return self._type

  @property
  def attendees(self):
    """
    All attendees invited to this event.

      Iterating over this property yields a list of :class:`ExchangeEventResponse` objects::

          for person in event.attendees:
            print person.name, person.response


      You can set the attendee list by assigning to this property::

          event.attendees = [u'somebody@somebody.foo',
                             u'somebodyelse@somebody.foo']

          event.update()

      If you add attendees this way, they will be required for the event.

      To add optional attendees, either use :attr:`optional_attendees` or add people using the :class:`ExchangeEventAttendee` object::

          from pyexchange.base import ExchangeEventAttendee

          attendee = ExchangeEventAttendee(name="Jane Doe",
                                           email="jane@her.email",
                                           required=False)

          event.attendees = attendee

          event.update()


      Attendees must have an email address defined.

    """

    # this is redundant in python 2, but necessary in python 3 - .values() returns dict_values, not a list
    return [attendee for attendee in self._attendees.values()]

  @attendees.setter
  def attendees(self, attendees):
    self._attendees = self._build_resource_dictionary(attendees)
    self._dirty_attributes.add(u'attendees')

  @property
  def required_attendees(self):
    """
    Required attendees for this event.

    This property otherwise behaves like :attr:`attendees`.
    """
    return [attendee for attendee in self._attendees.values() if attendee.required]

  @required_attendees.setter
  def required_attendees(self, attendees):
    required = self._build_resource_dictionary(attendees, required=True)

    # TODO rsanders medium. This is clunky - have to get around python 2/3 inconsistences :/
    # must be a better way to do it.

    # Diff the list of required people and drop anybody who wasn't included
    for attendee in self.required_attendees:
      if attendee.email not in required.keys():
        del self._attendees[attendee.email]

    # then add everybody to the list
    for email in required:
      self._attendees[email] = required[email]

    self._dirty_attributes.add(u'attendees')

  @property
  def optional_attendees(self):
    """
    Optional attendees for this event.

    This property otherwise behaves like :attr:`attendees`.
    """
    return [attendee for attendee in self._attendees.values() if not attendee.required]

  @optional_attendees.setter
  def optional_attendees(self, attendees):
    optional = self._build_resource_dictionary(attendees, required=False)

    # TODO rsanders medium. This is clunky - have to get around python 2/3 inconsistences :/
    # must be a better way to do it.

    # Diff the list of required people and drop anybody who wasn't included
    for attendee in self.optional_attendees:
      if attendee.email not in optional.keys():
        del self._attendees[attendee.email]

    # then add everybody to the list
    for email in optional:
      self._attendees[email] = optional[email]

    self._dirty_attributes.add(u'attendees')

  def add_attendees(self, attendees, required=True):
    """
    Adds new attendees to the event.

    *attendees* can be a list of email addresses or :class:`ExchangeEventAttendee` objects.
    """

    new_attendees = self._build_resource_dictionary(attendees, required=required)

    for email in new_attendees:
      self._attendees[email] = new_attendees[email]

    self._dirty_attributes.add(u'attendees')

  def remove_attendees(self, attendees):
    """
    Removes attendees from the event.

    *attendees* can be a list of email addresses or :class:`ExchangeEventAttendee` objects.
    """

    attendees_to_delete = self._build_resource_dictionary(attendees)
    for email in attendees_to_delete.keys():
      if email in self._attendees:
        del self._attendees[email]

    self._dirty_attributes.add(u'attendees')

  @property
  def resources(self):
    """
    Resources (aka conference rooms) for this event.

    This property otherwise behaves like :attr:`attendees`.
    """
    # this is redundant in python 2, but necessary in python 3 - .values() returns dict_values, not a list
    return [resource for resource in self._resources.values()]

  @resources.setter
  def resources(self, resources):
    self._resources = self._build_resource_dictionary(resources)
    self._dirty_attributes.add(u'resources')

  def add_resources(self, resources):
    """
    Adds new resources to the event.

    *resources* can be a list of email addresses or :class:`ExchangeEventAttendee` objects.
    """
    new_resources = self._build_resource_dictionary(resources)

    for key in new_resources:
      self._resources[key] = new_resources[key]
    self._dirty_attributes.add(u'resources')

  def remove_resources(self, resources):
    """
    Removes resources from the event.

    *resources* can be a list of email addresses or :class:`ExchangeEventAttendee` objects.
    """

    resources_to_delete = self._build_resource_dictionary(resources)
    for email in resources_to_delete.keys():
      if email in self._resources:
        del self._resources[email]

    self._dirty_attributes.add(u'resources')

  @property
  def conference_room(self):
    """ Alias to resources - Exchange calls 'em resources, but this is clearer"""
    if self.resources and len(self.resources) == 1:
      return self.resources[0]

  def validate(self):
    """ Validates that all required fields are present """
    if not self.start:
      raise ValueError("Event has no start date")

    if not self.end:
      raise ValueError("Event has no end date")

    if self.end < self.start:
      raise ValueError("End date is after start date")

    if self.reminder_minutes_before_start and not isinstance(self.reminder_minutes_before_start, int):
      raise TypeError("reminder_minutes_before_start must be of type int")

    if self.is_all_day and not isinstance(self.is_all_day, bool):
      raise TypeError("is_all_day must be of type bool")

  def create(self):
    raise NotImplementedError

  def update(self, send_only_to_changed_attendees=True):
    raise NotImplementedError

  def cancel(self):
    raise NotImplementedError

  def resend_invitations(self):
    raise NotImplementedError

  def get_master(self):
    raise NotImplementedError

  def get_occurrance(self, instance_index):
    raise NotImplementedError

  def as_json(self):
    """ Output ourselves as JSON """
    return json.dumps(self.__getstate__())

  def __getstate__(self):
    """ Implemented so pickle.dumps() and pickle.loads() work """
    state = {}
    for attribute in self.DATA_ATTRIBUTES:
      state[attribute] = getattr(self, attribute, None)
    return state

  def _build_resource_dictionary(self, resources, required=True):
    result = {}
    if resources:
      item_list = resources if isinstance(resources, list) else [resources]
      for item in item_list:
        if isinstance(item, ExchangeEventAttendee):
          if item.email is None:
            raise ValueError(u"You tried to add a resource or attendee with a blank email: {0}".format(item))

          result[item.email] = ExchangeEventResponse(email=item.email, required=item.required, name=item.name, response=None, last_response=None)
        elif isinstance(item, ExchangeEventResponse):
          if item.email is None:
            raise ValueError(u"You tried to add a resource or attendee with a blank email: {0}".format(item))

          result[item.email] = item
        else:
          if item is None:
            raise ValueError(u"You tried to add a resource or attendee with a blank email.")

          result[item] = ExchangeEventResponse(email=item, required=required, name=None, response=None, last_response=None)

    return result

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
