PyExchange
===================

PyExchange is a library for Microsoft Exchange.

It's incomplete at the moment - it only handles calendar events. We've open sourced it because we found it useful and hope others will, too.

If you're interested, please see the CONTRIBUTING notes in the repo for hints on where to get started.

Installation
------------

PyExchange supports Python 2.6 and 2.7. Our code is compatible with 3.3+, but see the notes below on getting it working. Non CPython implementations may work but are not tested.

We support Exchange Server version 2010. Others will likely work but are not tested.

To install, use pip::

    pip install pyexchange

PyExchange requires [lxml](http://lxml.de) for XML handling. This will be installed by pip on most systems. If you run into problems, please see lxml's [installation instructions](http://lxml.de/installation.html).

To install from source, download the source code, then run::

    python setup.py install


Python 3
--------

We use the library [python-ntlm](https://code.google.com/p/python-ntlm/) for authentication. As of July 2013, they have an experimental Python 3 port but it's not in PyPI for easy download.

To the best of our knowledge, PyExchange works with this port and is Python 3.3 compatible. But since this isn't easily testable, we can't officially support Python 3 at the moment. 

Help in this area would be appreciated.

About
-----

Once upon a time there was a beautiful princess, who just wanted to connect  her web application to the royal Microsoft Exchange server. She sent out her knights to find her an appropriate Python library, but none returned. 

So she decided to make her own.

The princess first tried all manner of SOAP libraries, but found them broken, or not unicode compliant, or plain just didn't work with Exchange. 

"This totally bites," said the princess. "I just need like four commands and I don't want to rule over an entire SOAP fork."

She then discovered Microsoft had excellent documentation on its Exchange services and had full XML samples. 

"Bitchin," said the princess, who had watched too many 80s movies recently. "I'll just write XML instead."

So she did, and it worked, and there was much feasting and celebration, followed by a royal battle with accounting over what constituted "reasonable" mead expenses.

And everybody lived happily ever after.

THE END


Documentation
-------------

For the most complete and up-to-date documentation, see **FIXME add read the docs url**.

