"""
(c) 2013 LinkedIn Corp. All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License");?you may not use this file except in compliance with the License. You may obtain a copy of the License at  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software?distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
# TODO get flake8 to just ignore the lines I want, dangit
# flake8: noqa

import logging
from ..base.calendar import BaseExchangeCalendarEvent, BaseExchangeCalendarService, ExchangeEventOrganizer, ExchangeEventResponse
from ..base.folder import BaseExchangeFolder, BaseExchangeFolderService
from ..base.soap import ExchangeServiceSOAP
from ..exceptions import FailedExchangeException, ExchangeStaleChangeKeyException, ExchangeItemNotFoundException, ExchangeInternalServerTransientErrorException, ExchangeIrresolvableConflictException

from . import soap_request

from lxml import etree

import warnings

log = logging.getLogger("pyexchange")


class Exchange2010Service(ExchangeServiceSOAP):

  def calendar(self, id="calendar"):
    return Exchange2010CalendarService(service=self, calendar_id=id)

  def mail(self):
    raise NotImplementedError("Sorry - nothin' here. Feel like adding it? :)")

  def contacts(self):
    raise NotImplementedError("Sorry - nothin' here. Feel like adding it? :)")

  def folder(self):
    return Exchange2010FolderService(service=self)

  def _send_soap_request(self, body, headers=None, retries=2, timeout=30, encoding="utf-8"):
    headers = {
      "Accept" : "text/xml",
      "Content-type" : "text/xml; charset=%s " % encoding
    }
    return super(Exchange2010Service, self)._send_soap_request(body, headers=headers, retries=retries, timeout=timeout, encoding=encoding)

  def _check_for_errors(self, xml_tree):
    super(Exchange2010Service, self)._check_for_errors(xml_tree)
    self._check_for_exchange_fault(xml_tree)

  def _check_for_exchange_fault(self, xml_tree):

    # If the request succeeded, we should see a <m:ResponseCode>NoError</m:ResponseCode>
    # somewhere in the response. if we don't (a) see the tag or (b) it doesn't say "NoError"
    # then flip out

    response_codes = xml_tree.xpath(u'//m:ResponseCode', namespaces=soap_request.NAMESPACES)

    if not response_codes:
      raise FailedExchangeException(u"Exchange server did not return a status response", None)

    # The full (massive) list of possible return responses is here.
    # http://msdn.microsoft.com/en-us/library/aa580757(v=exchg.140).aspx
    for code in response_codes:
      if code.text == u"ErrorChangeKeyRequiredForWriteOperations":
        # change key is missing or stale. we can fix that, so throw a special error
        raise ExchangeStaleChangeKeyException(u"Exchange Fault (%s) from Exchange server" % code.text)
      elif code.text == u"ErrorItemNotFound":
        # exchange_invite_key wasn't found on the server
        raise ExchangeItemNotFoundException(u"Exchange Fault (%s) from Exchange server" % code.text)
      elif code.text == u"ErrorIrresolvableConflict":
        # tried to update an item with an old change key
        raise ExchangeIrresolvableConflictException(u"Exchange Fault (%s) from Exchange server" % code.text)
      elif code.text == u"ErrorInternalServerTransientError":
        # temporary internal server error. throw a special error so we can retry
        raise ExchangeInternalServerTransientErrorException(u"Exchange Fault (%s) from Exchange server" % code.text)
      elif code.text != u"NoError":
        raise FailedExchangeException(u"Exchange Fault (%s) from Exchange server" % code.text)


class Exchange2010CalendarService(BaseExchangeCalendarService):

  def event(self, id=None, **kwargs):
    return Exchange2010CalendarEvent(service=self.service, id=id, **kwargs)

  def get_event(self, id):
    return Exchange2010CalendarEvent(service=self.service, id=id)

  def new_event(self, **properties):
    return Exchange2010CalendarEvent(service=self.service, calendar_id=self.calendar_id, **properties)

  def list_events(self, start=None, end=None, details=False, delegate_for=None):
    return Exchange2010CalendarEventList(service=self.service, start=start, end=end, details=details, delegate_for=None)


class Exchange2010CalendarEventList(object):
  """
  Creates & Stores a list of Exchange2010CalendarEvent items in the "self.events" variable.
  """
  def __init__(self, service=None, start=None, end=None, details=False, delegate_for=None):
    self.service = service
    self.count = 0
    self.start = start
    self.end = end
    self.events = list()
    self.event_ids = list()
    self.details = details

    # This request uses a Calendar-specific query between two dates.
    body = soap_request.get_calendar_items(format=u'AllProperties', start=self.start, end=self.end, delegate_for=self.delegate_for)
    response_xml = self.service.send(body)
    self._parse_response_for_all_events(response_xml)

    # Populate the event ID list, for convenience reasons.
    for event in self.events:
      self.event_ids.append(event._id)

    # If we have requested all the details, basically repeat the previous 3 steps,
    # but instead of start/stop, we have a list of ID fields.
    if self.details:
      log.debug(u'Received request for all details, retrieving now!')
      self.load_all_details()
    return

  def _parse_response_for_all_events(self, response):
    """
    This function will retrieve *most* of the event data, excluding Organizer & Attendee details
    """
    calendar_items = response.xpath(u'//t:CalendarItem', namespaces=soap_request.NAMESPACES)
    counter = 0
    if calendar_items:
      self.count = len(calendar_items)
      log.debug(u'Found %s items' % self.count)
      
      for item in calendar_items:
        # Skip matches of CalendarItem that are contained within other CalenderItems, particularly
        # the fact that "<CalendarItem>" tags are located within "<ConflictingMeetings>"
        if item.getparent().tag.endswith('ConflictingMeetings'):
          continue

        self._add_event(xml=item)
    else:
      log.debug(u'No calendar items found with search parameters.')

    return self
  
  def _add_event(self, xml=None):
    log.debug(u'Adding new event to all events list.')
    event = Exchange2010CalendarEvent(service=self.service, xml=xml)
    log.debug(u'Subject of new event is %s' % event.subject)
    self.events.append(event)
    return self

  def load_all_details(self):
    """
    This function will execute all the event lookups for known events.

    This is intended for use when you want to have a completely populated event entry, including
    Organizer & Attendee details.
    """
    log.debug(u"Loading all details")
    if self.count > 0:
      # Now, empty out the events to prevent duplicates!
      del(self.events[:])
      
      # Send the SOAP request with the list of exchange ID values.
      log.debug(u"Requesting all event details for events: {event_list}".format(event_list=str(self.event_ids)))
      body = soap_request.get_item(exchange_id=self.event_ids, format=u'AllProperties')
      response_xml = self.service.send(body)

      # Re-parse the results for all the details!
      self._parse_response_for_all_events(response_xml)
    
    return self


class Exchange2010CalendarEvent(BaseExchangeCalendarEvent):

  def _init_from_service(self, id):
    log.debug(u'Creating new Exchange2010CalendarEvent object from ID')
    self.xpath_root = u'//m:Items/t:CalendarItem'
    body = soap_request.get_item(exchange_id=id, format=u'AllProperties')
    response_xml = self.service.send(body)
    properties = self._parse_response_for_get_event(response_xml)

    self._update_properties(properties)
    self._id = id
    log.debug(u'Created new event object with ID: %s' % self._id)

    self._reset_dirty_attributes()

    return self

  def _init_from_xml(self, xml=None):
    log.debug(u'Creating new Exchange2010CalendarEvent object from XML')
    self.xpath_root = u'.'
    properties = self._parse_event_properties(xml)

    self._update_properties(properties)
    self._id = xml.xpath(u'./t:ItemId/@Id', namespaces=soap_request.NAMESPACES)[0]

    log.debug(u'Created new event object with ID: %s' % self._id)
    self._reset_dirty_attributes()

    return self

  def as_json(self):
    raise NotImplementedError

  def create(self):
    """
    Creates an event in Exchange. ::

        event = service.calendar().new_event(
          subject=u"80s Movie Night",
          location = u"My house",
        )
        event.create()

    Invitations to attendees are sent out immediately.

    """
    self.validate()
    body = soap_request.new_event(self)

    response_xml = self.service.send(body)
    self._id, self._change_key = self._parse_id_and_change_key_from_response(response_xml)

    return self

  def resend_invitations(self):
    """
    Resends invites for an event.  ::

        event = service.calendar().get_event(id='KEY HERE')
        event.resend_invitations()

    Anybody who has not declined this meeting will get a new invite.
    """

    if not self.id:
      raise TypeError(u"You can't send invites for an event that hasn't been created yet.")

    # Under the hood, this is just an .update() but with no attributes changed.
    # We're going to enforce that by checking if there are any changed attributes and bail if there are
    if self._dirty_attributes:
      raise ValueError(u"There are unsaved changes to this invite - please update it first: %r" % self._dirty_attributes)

    self.refresh_change_key()
    body = soap_request.update_item(self, [], calendar_item_update_operation_type=u'SendOnlyToAll')
    self.service.send(body)

    return self

  def update(self, calendar_item_update_operation_type=u'SendToAllAndSaveCopy', **kwargs):
    """
    Updates an event in Exchange.  ::

        event = service.calendar().get_event(id='KEY HERE')
        event.location = u'New location'
        event.update()

    If no changes to the event have been made, this method does nothing.

    Notification of the change event is sent to all users. If you wish to just notify people who were
    added, specify ``send_only_to_changed_attendees=True``.
    """
    if not self.id:
      raise TypeError(u"You can't update an event that hasn't been created yet.")

    if 'send_only_to_changed_attendees' in kwargs:
      warnings.warn(
        "The argument send_only_to_changed_attendees is deprecated.  Use calendar_item_update_operation_type instead.",
        DeprecationWarning,
      )  # 20140502
      if kwargs['send_only_to_changed_attendees']:
        calendar_item_update_operation_type = u'SendToChangedAndSaveCopy'

    VALID_UPDATE_OPERATION_TYPES = (
      u'SendToNone', u'SendOnlyToAll', u'SendOnlyToChanged',
      u'SendToAllAndSaveCopy', u'SendToChangedAndSaveCopy',
    )
    if calendar_item_update_operation_type not in VALID_UPDATE_OPERATION_TYPES:
      raise ValueError('calendar_item_update_operation_type has unknown value')

    self.validate()

    if self._dirty_attributes:
      log.debug(u"Updating these attributes: %r" % self._dirty_attributes)
      self.refresh_change_key()

      body = soap_request.update_item(self, self._dirty_attributes, calendar_item_update_operation_type=calendar_item_update_operation_type)
      self.service.send(body)
      self._reset_dirty_attributes()
    else:
      log.info(u"Update was called, but there's nothing to update. Doing nothing.")

    return self

  def cancel(self):
    """
    Cancels an event in Exchange.  ::

        event = service.calendar().get_event(id='KEY HERE')
        event.cancel()

    This will send notifications to anyone who has not declined the meeting.
    """
    if not self.id:
      raise TypeError(u"You can't delete an event that hasn't been created yet.")

    self.refresh_change_key()
    self.service.send(soap_request.delete_event(self))
    # TODO rsanders high - check return status to make sure it was actually sent
    return None

  def move_to(self, folder_id):
    """
    :param str folder_id: The Calendar ID to where you want to move the event to.
    Moves an event to a different folder (calendar).  ::

      event = service.calendar().get_event(id='KEY HERE')
      event.move_to(folder_id='NEW CALENDAR KEY HERE')
    """
    if not folder_id:
      raise TypeError(u"You can't move an event to a non-existant folder")

    if not isinstance(folder_id, basestring):
      raise TypeError(u"folder_id must be a string")

    if not self.id:
      raise TypeError(u"You can't move an event that hasn't been created yet.")

    self.refresh_change_key()
    response_xml = self.service.send(soap_request.move_event(self, folder_id))
    new_id, new_change_key = self._parse_id_and_change_key_from_response(response_xml)
    if not new_id:
      raise ValueError(u"MoveItem returned success but requested item not moved")

    self._id = new_id
    self._change_key = new_change_key
    self.calendar_id = folder_id
    return self

  def refresh_change_key(self):

    body = soap_request.get_item(exchange_id=self._id, format=u"IdOnly")
    response_xml = self.service.send(body)
    self._id, self._change_key = self._parse_id_and_change_key_from_response(response_xml)

    return self

  def _parse_id_and_change_key_from_response(self, response):

    id_elements = response.xpath(u'//m:Items/t:CalendarItem/t:ItemId', namespaces=soap_request.NAMESPACES)

    if id_elements:
      id_element = id_elements[0]
      return id_element.get(u"Id", None), id_element.get(u"ChangeKey", None)
    else:
      return None, None

  def _parse_response_for_get_event(self, response):

    result = self._parse_event_properties(response)

    organizer_properties = self._parse_event_organizer(response)
    result[u'organizer'] = ExchangeEventOrganizer(**organizer_properties)

    attendee_properties = self._parse_event_attendees(response)
    result[u'_attendees'] = self._build_resource_dictionary([ExchangeEventResponse(**attendee) for attendee in attendee_properties])

    resource_properties = self._parse_event_resources(response)
    result[u'_resources'] = self._build_resource_dictionary([ExchangeEventResponse(**resource) for resource in resource_properties])

    return result

  def _parse_event_properties(self, response):

    property_map = {
      u'subject'      : { u'xpath' : self.xpath_root + u'/t:Subject'},  # noqa
      u'location'     : { u'xpath' : self.xpath_root + u'/t:Location'},  # noqa
      u'availability' : { u'xpath' : self.xpath_root + u'/t:LegacyFreeBusyStatus'},  # noqa
      u'start'        : { u'xpath' : self.xpath_root + u'/t:Start', u'cast': u'datetime'},  # noqa
      u'end'          : { u'xpath' : self.xpath_root + u'/t:End', u'cast': u'datetime'},  # noqa
      u'html_body'    : { u'xpath' : self.xpath_root + u'/t:Body[@BodyType="HTML"]'},  # noqa
      u'text_body'    : { u'xpath' : self.xpath_root + u'/t:Body[@BodyType="Text"]'},  # noqa
      u'reminder_minutes_before_start'  : { u'xpath' : self.xpath_root + u'/t:ReminderMinutesBeforeStart', u'cast': u'int'},  # noqa
      u'is_all_day'   : { u'xpath' : self.xpath_root + u'/t:IsAllDayEvent', u'cast': u'bool'},  # noqa
    }

    return self.service._xpath_to_dict(element=response, property_map=property_map, namespace_map=soap_request.NAMESPACES)

  def _parse_event_organizer(self, response):

    organizer = response.xpath(self.xpath_root + u'/t:Organizer/t:Mailbox', namespaces=soap_request.NAMESPACES)

    property_map = {
      u'name'      : { u'xpath' : u't:Name'},  # noqa
      u'email'     : { u'xpath' : u't:EmailAddress'},  # noqa
    }

    if organizer:
      return self.service._xpath_to_dict(element=organizer[0], property_map=property_map, namespace_map=soap_request.NAMESPACES)
    else:
      return None

  def _parse_event_resources(self, response):
    property_map = {
      u'name'         : { u'xpath' : u't:Mailbox/t:Name'},  # noqa
      u'email'        : { u'xpath' : u't:Mailbox/t:EmailAddress'},  # noqa
      u'response'     : { u'xpath' : u't:ResponseType'},  # noqa
      u'last_response': { u'xpath' : u't:LastResponseTime', u'cast': u'datetime'},  # noqa
    }

    result = []

    resources = response.xpath(self.xpath_root + u'/t:Resources/t:Attendee', namespaces=soap_request.NAMESPACES)

    for attendee in resources:
      attendee_properties = self.service._xpath_to_dict(element=attendee, property_map=property_map, namespace_map=soap_request.NAMESPACES)
      attendee_properties[u'required'] = True

      if u'last_response' not in attendee_properties:
        attendee_properties[u'last_response'] = None

      result.append(attendee_properties)

    return result

  def _parse_event_attendees(self, response):

    property_map = {
      u'name'         : { u'xpath' : u't:Mailbox/t:Name'},  # noqa
      u'email'        : { u'xpath' : u't:Mailbox/t:EmailAddress'},  # noqa
      u'response'     : { u'xpath' : u't:ResponseType'},  # noqa
      u'last_response': { u'xpath' : u't:LastResponseTime', u'cast': u'datetime'},  # noqa
    }

    result = []

    required_attendees = response.xpath(self.xpath_root + u'/t:RequiredAttendees/t:Attendee', namespaces=soap_request.NAMESPACES)
    for attendee in required_attendees:
      attendee_properties = self.service._xpath_to_dict(element=attendee, property_map=property_map, namespace_map=soap_request.NAMESPACES)
      attendee_properties[u'required'] = True

      if u'last_response' not in attendee_properties:
        attendee_properties[u'last_response'] = None

      result.append(attendee_properties)

    optional_attendees = response.xpath(self.xpath_root + u'/t:OptionalAttendees/t:Attendee', namespaces=soap_request.NAMESPACES)

    for attendee in optional_attendees:
      attendee_properties = self.service._xpath_to_dict(element=attendee, property_map=property_map, namespace_map=soap_request.NAMESPACES)
      attendee_properties[u'required'] = False

      if u'last_response' not in attendee_properties:
        attendee_properties[u'last_response'] = None

      result.append(attendee_properties)

    return result


class Exchange2010FolderService(BaseExchangeFolderService):

  def folder(self, id=None, **kwargs):
    return Exchange2010Folder(service=self.service, id=id, **kwargs)

  def get_folder(self, id):
    """
      :param str id:  The Exchange ID of the folder to retrieve from the Exchange store.

      Retrieves the folder specified by the id, from the Exchange store.

      **Examples**::

        folder = service.folder().get_folder(id)

    """

    return Exchange2010Folder(service=self.service, id=id)

  def new_folder(self, **properties):
    """
      new_folder(display_name=display_name, folder_type=folder_type, parent_id=parent_id)
      :param str display_name:  The display name given to the new folder.
      :param str folder_type:  The type of folder to create.  Possible values are 'Folder',
        'CalendarFolder', 'ContactsFolder', 'SearchFolder', 'TasksFolder'.
      :param str parent_id:  The parent folder where the new folder will be created.

      Creates a new folder with the given properties.  Not saved until you call the create() method.

      **Examples**::

        folder = service.folder().new_folder(
          display_name=u"New Folder Name",
          folder_type="CalendarFolder",
          parent_id='calendar',
        )
        folder.create()

    """

    return Exchange2010Folder(service=self.service, **properties)

  def find_folder(self, parent_id):
    """
      find_folder(parent_id)
      :param str parent_id:  The parent folder to list.

      This method will return a list of sub-folders to a given parent folder.

      **Examples**::

        # Iterate through folders within the default 'calendar' folder.
        folders = service.folder().find_folder(parent_id='calendar')
        for folder in folders:
          print(folder.display_name)

        # Delete all folders within the 'calendar' folder.
        folders = service.folder().find_folder(parent_id='calendar')
        for folder in folders:
          folder.delete()
    """

    body = soap_request.find_folder(parent_id=parent_id, format=u'AllProperties')
    response_xml = self.service.send(body)
    return self._parse_response_for_find_folder(response_xml)

  def _parse_response_for_find_folder(self, response):

    result = []
    folders = response.xpath(u'//t:Folders/t:*', namespaces=soap_request.NAMESPACES)
    for folder in folders:
      result.append(
        Exchange2010Folder(
          service=self.service,
          xml=etree.fromstring(etree.tostring(folder))  # Might be a better way to do this
        )
      )

    return result


class Exchange2010Folder(BaseExchangeFolder):

  def _init_from_service(self, id):

    body = soap_request.get_folder(folder_id=id, format=u'AllProperties')
    response_xml = self.service.send(body)
    properties = self._parse_response_for_get_folder(response_xml)

    self._update_properties(properties)

    return self

  def _init_from_xml(self, xml):

    properties = self._parse_response_for_get_folder(xml)
    self._update_properties(properties)

    return self

  def create(self):
    """
    Creates a folder in Exchange. ::

      calendar = service.folder().new_folder(
        display_name=u"New Folder Name",
        folder_type="CalendarFolder",
        parent_id='calendar',
      )
      calendar.create()
    """

    self.validate()
    body = soap_request.new_folder(self)

    response_xml = self.service.send(body)
    self._id, self._change_key = self._parse_id_and_change_key_from_response(response_xml)

    return self

  def delete(self):
    """
    Deletes a folder from the Exchange store. ::

      folder = service.folder().get_folder(id)
      print("Deleting folder: %s" % folder.display_name)
      folder.delete()
    """

    if not self.id:
      raise TypeError(u"You can't delete a folder that hasn't been created yet.")

    body = soap_request.delete_folder(self)

    response_xml = self.service.send(body)  # noqa
    # TODO: verify deletion
    self._id = None
    self._change_key = None

    return None

  def move_to(self, folder_id):
    """
    :param str folder_id: The Folder ID of what will be the new parent folder, of this folder.
    Move folder to a different location, specified by folder_id::

      folder = service.folder().get_folder(id)
      folder.move_to(folder_id="ID of new location's folder")
    """

    if not folder_id:
      raise TypeError(u"You can't move to a non-existant folder")

    if not isinstance(folder_id, basestring):
      raise TypeError(u"folder_id must be a string")

    if not self.id:
      raise TypeError(u"You can't move a folder that hasn't been created yet.")

    response_xml = self.service.send(soap_request.move_folder(self, folder_id))  # noqa

    result_id, result_key = self._parse_id_and_change_key_from_response(response_xml)
    if self.id != result_id:
      raise ValueError(u"MoveFolder returned success but requested folder not moved")

    self.parent_id = folder_id
    return self

  def _parse_response_for_get_folder(self, response):
    FOLDER_PATH = u'//t:Folder | //t:CalendarFolder | //t:ContactsFolder | //t:SearchFolder | //t:TasksFolder'

    path = response.xpath(FOLDER_PATH, namespaces=soap_request.NAMESPACES)[0]
    result = self._parse_folder_properties(path)
    return result

  def _parse_folder_properties(self, response):

    property_map = {
      u'display_name'       : { u'xpath' : u't:DisplayName'},
    }

    self._id, self._change_key = self._parse_id_and_change_key_from_response(response)
    self._parent_id = self._parse_parent_id_and_change_key_from_response(response)[0]
    self.folder_type = etree.QName(response).localname

    return self.service._xpath_to_dict(element=response, property_map=property_map, namespace_map=soap_request.NAMESPACES)

  def _parse_id_and_change_key_from_response(self, response):

    id_elements = response.xpath(u'//t:FolderId', namespaces=soap_request.NAMESPACES)

    if id_elements:
      id_element = id_elements[0]
      return id_element.get(u"Id", None), id_element.get(u"ChangeKey", None)
    else:
      return None, None

  def _parse_parent_id_and_change_key_from_response(self, response):

    id_elements = response.xpath(u'//t:ParentFolderId', namespaces=soap_request.NAMESPACES)

    if id_elements:
      id_element = id_elements[0]
      return id_element.get(u"Id", None), id_element.get(u"ChangeKey", None)
    else:
      return None, None
