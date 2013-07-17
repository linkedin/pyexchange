PyExchange
==========

.. module:: pyexchange

PyExchange is a library for Microsoft Exchange.

It's incomplete at the moment - it only handles calendar events. We've open sourced it because we found it useful and hope others will, too.

If you're interested in helping us extend it, please see the :doc:`notes on contributing </contributing>` for hints on where to get started, or contact us.

Installation
------------

PyExchange supports Python 2.6 and 2.7. Our code is compatible with 3.3+, but see the notes below on getting it working. Non CPython implementations may work but are not tested.

We support Exchange Server version 2010. Others will likely work but are not tested.

To install, use pip::

    pip install pyexchange

PyExchange requires `lxml <http://lxml.de>`_ for XML handling. This will be installed by pip on most systems. If you run into problems, please see lxml's `installation instructions <http://lxml.de/installation.html>`_.

To install from source, download the source code, then run::

    python setup.py install

Python 3
````````

We depend on the library `python-ntlm <https://code.google.com/p/python-ntlm/>`_ for authentication. As of July 2013, they have an experimental Python 3 port but it's not in PyPI for easy download.

Help in this area would be appreciated.

Introduction
------------

Once upon a time there was a beautiful princess, who wanted to connect her web application to the royal Microsoft Exchange server.

The princess first tried all manner of SOAP libraries, but found them broken, or slow, or not unicode compliant, or plain just didn't work with Exchange.

"This totally bites," said the princess. "I need like four commands and I don't want to make my own SOAP library."

She then discovered Microsoft had excellent documentation on its Exchange services with full XML samples.

"Bitchin," said the princess, who had watched too many 80s movies recently. "I'll just write XML instead."

So she did, and it worked, and there was much feasting and celebration, followed by a royal battle with accounting over what constituted reasonable mead expenses.

And everybody lived happily ever after.

THE END

Quickstart
----------

You can get, create, modify, and delete calendar events.

To work with any existing event, you must know its unique identifier in Exchange. For more information, see the `MSDN Exchange Web Services documentation <http://msdn.microsoft.com/en-us/library/aa580234(v=exchg.140).aspx>`_.

Setting up the connection
`````````````````````````

To do anything in Exchange, you first need to create the Exchange service object::

   from pyexchange import Exchange2010Service, ExchangeNTLMAuthConnection

    URL = u'https://your.email.server.com.here/EWS/Exchange.asmx'
    USERNAME = u'YOURDOMAIN\\yourusername'
    PASSWORD = u"12345? That's what I have on my luggage!"

    # Set up the connection to Exchange
    connection = ExchangeNTLMAuthConnection(url=URL,
                                            username=USERNAME,
                                            password=PASSWORD)

    service = Exchange2010Service(connection)

Creating an event
`````````````````
To create an event, use the ``new_event`` method::

    # You can set event properties when you instantiate the event...
    event = service.calendar().new_event(
      subject=u"80s Movie Night",
      attendees=[u'your_friend@friendme.domain', u'your_other_friend@their.domain'],
      location = u"My house",
    )

    # ...or afterwards
    event.start=datetime(2013,1,1,15,0,0, tzinfo=timezone("US/Pacific")),
    event.end=datetime(2013,1,1,21,0,0, tzinfo=timezone("US/Pacific"))

    event.html_body = u"""<html>
        <body>
            <h1>80s Movie night</h1>
            <p>We're watching Spaceballs, Wayne's World, and
            Bill and Ted's Excellent Adventure.</p>
            <p>PARTY ON DUDES!</p>
        </body>
    </html>"""

    # Connect to Exchange and create the event
    event.create()

For a full list of fields, see the :class:`.Exchange2010CalendarEvent` documentation.

When you create an event, Exchange creates a unique identifier for it. You need this key to get the event later.

After you create the object, the ``id`` attribute is populated with the key::

    print event.id  # prints None

    # Create the event
    event.create()

    print event.id # prints Exchange key

If you save this key, be warned the keys are quite long - easily 130+ characters.

If we could not create the event, a ``pyexchange.exceptions.FailedExchangeException`` exception is thrown.

Getting an event
````````````````

To get an existing event, you'll need its Exchange id.

Then get the event using the ``get_event`` method::

    EXCHANGE_ID = u'3123132131231231'

    event = service.calendar().get_event(id=EXCHANGE_ID)

    print event.id  # the same as EXCHANGE_ID
    print event.subject
    print event.location

    print event.start # datetime object
    print event.end # datetime object

    print event.body

    for person in event.attendees:
      print person.name
      print person.email
      print person.response # Accepted/Declined

If the id doesn't match anything in Exchange, a ``pyexchange.exceptions.ExchangeItemNotFoundException`` exception is thrown.

For all other errors, we throw a ``pyexchange.exceptions.FailedExchangeException``.

Modifying an event
``````````````````

To modify an event, first get the event::

    EXCHANGE_ID = u'3123132131231231'

    event = service.calendar().get_event(id=EXCHANGE_ID)

Then simply assign to the properties you want to change and use ``update``::

    event.location = u'New location'
    event.attendees = [u'thing1@dr.suess', u'thing2@dr.suess']

    event.update()

If the id doesn't match anything in Exchange, a ``pyexchange.exceptions.ExchangeItemNotFoundException`` exception is thrown.

For all other errors, we throw a ``pyexchange.exceptions.FailedExchangeException``.

Cancelling an event
```````````````````

To cancel an event, simply do::

    event = my_calendar.get_event(id=EXCHANGE_ID)

    event.cancel()

If the id doesn't match anything in Exchange, a ``pyexchange.exceptions.ExchangeItemNotFoundException`` exception is thrown.

For all other errors, we throw a ``pyexchange.exceptions.FailedExchangeException``.

Resending invitations
`````````````````````

To resend invitations to all participants, do::

    event = my_calendar.get_event(id=EXCHANGE_ID)

    event.resend_invitations()

Other tips and tricks
`````````````````````

You can pickle events if you need to serialize them. (We do this to send invites asynchronously.) ::

    import pickle

    # ...create event

    print event.subject
    pickled_event = pickle.dumps(event)

    rehydrated_event = pickle.loads(pickled_event)
    print rehydrated_event.subject # same as before


Changelog
---------

* :doc:`changelog </changelog>`

Support
-------

To report bugs or get support, please use the Github issue tracker.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

