Contributing
============

Hi! Thanks so much for wanting to contribute.

Setting up for development
--------------------------

There's a few extra steps to set up for development.

Installing from source
``````````````````````

To install in development mode from source, download the source code, then run this::

    python setup.py develop

Installing libraries
````````````````````

To do development work, you'll need a few more libraries::

    pip install -r dev_requirements.txt

Running the tests
`````````````````

Make sure you have the development libraries installed, then run::

    nosetests

Building documentation
``````````````````````

Make sure you have the development libraries installed, then do::

    cd docs
    make html

The generated documentation will be in ``docs/_build/html/``.

Guidelines
----------

Style guide
```````````

The code follows `PEP8
<http://www.python.org/dev/peps/pep-0008/>`_ with the following exceptions:

* Indentation is 2 spaces (no tabs)
* Line length: use your best judgment. (We all have big monitors now, no need to limit to 80 columns.)

Your code should pass `flake8
<http://flake8.readthedocs.org/>`_ unless readability is hurt, you have a good reason, or we really like you. Configuration is in ``setup.cfg``.

Python 3
````````

If possible, your code should be compatible with Python 3.3.


Tests
`````

Submitted code should have tests covering the code submitted.

All fixture data should be unicode, following the guidelines in Ned Batchelder's fantastic `Pragmatic Unicode <http://nedbatchelder.com/text/unipain.html>`_.

For example, instead of using the string ``"Test string"``, use ``u"tëst strïnġ"``. This will catch unicode
problems up front, saving a world of pain later.

Google "weirdmaker" for many, many obnoxious sites where you can do this conversion
automatically.

Ideas for how to contribute
---------------------------

If you don't know where to start, documentation is always welcome.

Microsoft has fantastic documentation on Exchange Web Services (EWS) SOAP request/responses. To add new functionality,
you'll need to find the action you want to add in their documentation. 

Start here: `Exchange Web Services Operations <http://msdn.microsoft.com/en-us/library/bb409286(v=exchg.140).aspx>`_

The existing codebase and that should get you started. Feel free to contact us for help. 

General areas for improvement are:

    * Python 3 support (updating python-ntlm would be great)
    * Support for more versions of Exchange
    * Extend calendar functionality
        - More fields
        - More actions
        - Add the ability to output events as JSON
    * Add mail functionality
    * Add contacts functionality



