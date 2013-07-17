Attendee
========

These are helper classes (`named tuples <http://docs.python.org/library/collections.html>`_, actually) to store data
about event organizers and attendee information.

.. toctree::
   :maxdepth: 2

.. class:: ExchangeEventAttendee

    When setting up attendees for an event, you can use this instead of an email address.

    .. attribute:: name

        The name of the person to invite.

    .. attribute:: email

        The email of the person to invite. **Required.**

    .. attribute:: required

        Boolean. True if this person is required, false if they are optional.


.. class:: ExchangeEventResponse

    This is returned when you iterate over attendees or resources of an event. It's populated from Exchange's information.

    .. attribute:: name

        The name of the person attending this event, if Exchange knows it.

    .. attribute:: email

        The attendee's email address. This will always be populated.

    .. attribute:: response

        The person's response. Will be one of::

            RESPONSE_ACCEPTED = u'Accept'
            RESPONSE_DECLINED = u'Decline'
            RESPONSE_TENTATIVE = u'Tentative'
            RESPONSE_UNKNOWN = u'Unknown'  # they have not yet replied

        The list of all possible values is in ``pyexchange.calendar.RESPONSES``.

    .. attribute:: last_response

        The datetime (UTC) of when they last responded to the invitation.

    .. attribute:: required

        Boolean. True if this person is required, false if they are optional.


.. class:: ExchangeEventOrganizer

    This is returned when you request the organizer of the event. It's populated from Exchange's information.

    .. attribute:: name

        The name of the person who created this event, if Exchange knows it.

    .. attribute:: email

        The email of the event organizer.
