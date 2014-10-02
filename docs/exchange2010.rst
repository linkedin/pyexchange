.. automodule:: pyexchange.exchange2010

.. toctree::
   :maxdepth: 2

Exchange2010CalendarEvent
=========================

.. autoclass:: Exchange2010CalendarEvent
    :members: create, update, cancel, resend_invitations

    .. attribute:: id

      **Read-only.** The internal id Exchange uses to refer to this event.

    .. attribute:: subject

      The subject or title of the event.

    .. attribute:: start

      The start time and date of the event. Should be a non-naive (i.e. with timezone) datetime object.

    .. attribute:: end

      The end time and date of the event. Should be a non-naive (i.e. with timezone) datetime object.

    .. attribute:: location

      The location of the event. This is a string.

    .. attribute:: html_body

      The HTML version of the message. Either this or :attr:`text_body` must be set.

    .. attribute:: text_body

      The text version of the message. Either this or :attr:`html_body` must be set.

    .. attribute:: body

      **Read-only.** Returns either :attr:`html_body` or :attr:`text_body`, whichever is set. If both are set, :attr:`html_body` is returned.

    .. attribute:: organizer

      **Read-only.** The organizer of the event.

      This returns a :class:`ExchangeEventOrganizer` object.

    .. attribute:: attendees

      All attendees invited to this event.

      Iterating over this property yields a list of :class:`ExchangeEventResponse` objects::

          for person in event.attendees:
            print person.name, person.response


      You can set the attendee list by assigning to this property::

          event.attendees = [u'somebody@company.foo',
                             u'somebodyelse@company.foo']

      If you add attendees this way, they will be required for the event.

      To add optional attendees, either use :attr:`optional_attendees` or add people using the :class:`ExchangeEventAttendee` object::

          from pyexchange.base import ExchangeEventAttendee

          attendee = ExchangeEventAttendee(name="Jane Doe",
                                           email="jane@her.email",
                                           required=False)

          event.attendees = attendee

      Attendees must have an email address defined.

    .. attribute:: required_attendees

      Required attendees for this event. ::

          event.required_attendees = [u'important_person@company.foo',
                                      u'admin@company.foo']

          for person in event.required_attendees:
            print person.email

      This property otherwise behaves like :attr:`attendees`.

    .. attribute:: optional_attendees

      Optional attendees for this event. ::

          event.optional_attendees = [u'maybe@company.foo',
                                      u'other_optional@company.foo']

          for person in event.optional_attendees:
            print person.email

      This property otherwise behaves like :attr:`attendees`.

    .. attribute:: resources

      Resources (aka conference rooms) for this event. ::

          event.resources = [u'conferenceroom@company.foo']

          for room in event.resources:
            print room.email

      This property otherwise behaves like :attr:`attendees`.

    .. attribute:: conference_room

      **Read-only.** A property to return the first resource, since the most common use case is a meeting
      with one resource (the conference room). ::

          event.resources = [u'conferenceroom@company.foo']

          print event.conference_room.email # u'conferenceroom@company.foo'

      Returns a :class:`ExchangeEventAttendee` object.

    .. method:: add_attendee(attendees, required=True)

      Adds new attendees to the event.

      *attendees* can be a list of email addresses or :class:`ExchangeEventAttendee` objects. ::

          event.attendees = [u'jane@company.foo',
                             u'jack@company.foo']
          event.add_attendee([u'chrissie@company.foo'])

          print len(event.attendees) # prints 3

      If *required* is true, attendees will be marked as required. Otherwise, they'll be optional.

    .. method:: remove_attendees(attendees)

      Removes attendees from the event. ::

          event.attendees = [u'jane@company.foo',
                             u'jack@company.foo',
                             u'chrissie@company.foo']
          event.remove_attendees([u'jack@company.foo', u'chrissie@company.foo'])

          print len(event.attendees) # prints 1

      *attendees* can be a list of email addresses or :class:`ExchangeEventAttendee` objects.

    .. method:: add_resources(resources)

      Adds new resources to the event. ::

          event.resources = [u'room@company.foo']
          event.add_resources([u'projector@company.foo'])

          print len(event.attendees) # prints 2

      *resources* can be a list of email addresses or :class:`ExchangeEventAttendee` objects.

    .. method:: remove_resources(resources)

      Removes resources from the event. ::

          event.resources = [u'room@company.foo',
                             u'projector@company.foo']
          event.remove_resources(u'projector@company.foo')

          print len(event.attendees) # prints 1

      *resources* can be a list of email addresses or :class:`ExchangeEventAttendee` objects.


Exchange2010FolderService
=========================

.. autoclass:: Exchange2010FolderService()
    :members: get_folder, new_folder, find_folder


Exchange2010Folder
=========================

.. autoclass:: Exchange2010Folder()
    :members: create, delete, move_to

    .. attribute:: id

      **Read-only.** The internal id Exchange uses to refer to this folder.

    .. attribute:: parent_id

      **Read-only.** The internal id Exchange uses to refer to the parent folder.

    .. attribute:: folder_type

      The type of folder this is.  Can be one of the following::

        'Folder', 'CalendarFolder', 'ContactsFolder', 'SearchFolder', 'TasksFolder'

    .. attribute:: display_name

      The name of the folder.
