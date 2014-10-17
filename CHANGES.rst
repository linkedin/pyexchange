Changes
=======

0.1 (June 24, 2013)
--------------------

Team release - shakin' the bugs out. 


0.2 (July 1, 2013)
--------------------

Internal company release - RELEASE THE KRAKEN.


0.3 (July 17, 2013)
------------------

Initial public release. 


0.3.1 (April 18, 2014)
----------------------

Integrating some more granular exception handling.

0.4 (June 2, 2014)
------------------

We had some great contributions, so this is a release for that. 

Alejandro Ramirez (got-root):

- Added functionality to create/delete/get/find/move folders of all types. (Creating a new CalendarFolder is creating a new calendar in exchange)
- Added ability to create events in specific folders.
- Added ability to move events between calendars (folders).
- Created tests for all new features. 

Ben Le (kantas92)

* Fixed unicode vs bytecode encoding madness when sending unicode.

0.4.1 (June 15, 2014)
------------------

Turns out I actually didn't release Ben Le's code when I thought I did. Bad release engineer, no biscuit. 

0.4.2 (October 3, 2014)
----------------------

Alejandro Ramirez (got-root):

- Bug fixes around the new folder code. 
- More documentation on how to use folders. 


0.5 (October 15, 2014)
----------------------

** This release has a potential backwards incompatible change, see below **

* Pyexchange uses requests under the hood now (@trustrachel)

    Hey did you know that requests can do NTLM? I didn't. The internal connection class now uses requests
    instead of the clunky urllib2.

    There's a backwards incompatible change if you're subclassing the connection object. Requests doesn't
    need nearly the crud that urllib2 did, so I changed some of the methods and properties.

    Almost nobody should use this feature, but beware if you do.

* You can get a list of events between two dates. This was a big limitation of the library before, so a huge
 thank you to Eric Matthews (@ematthews))

* Fixed bug causing retrieved events to not be in UTC. (Thanks to Alejandro Ramirez (@got-root))

* Integrated with travis (finally).





