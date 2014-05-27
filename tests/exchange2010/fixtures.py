# -*- coding: utf-8 -*-
"""
(c) 2013 LinkedIn Corp. All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License");?you may not use this file except in compliance with the License. You may obtain a copy of the License at  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software?distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
from datetime import datetime, timedelta
from collections import namedtuple
from pyexchange.base.calendar import ExchangeEventOrganizer, ExchangeEventResponse, RESPONSE_ACCEPTED, RESPONSE_DECLINED, RESPONSE_TENTATIVE, RESPONSE_UNKNOWN
from pyexchange.exchange2010.soap_request import EXCHANGE_DATE_FORMAT

# don't remove this - a few tests import stuff this way
from ..fixtures import *

EventFixture = namedtuple('EventFixture', ['id', 'change_key', 'subject', 'location', 'start', 'end', 'body'])
FolderFixture = namedtuple('FolderFixture', ['id', 'change_key', 'display_name', 'parent_id', 'folder_type'])

TEST_FOLDER = FolderFixture(
  id=u'AABBCCDDEEFF',
  change_key=u'GGHHIIJJKKLLMM',
  display_name=u'Conference Room ★',
  parent_id=u'FFEEDDCCBBAA',
  folder_type=u'Folder',
)

TEST_EVENT = EventFixture(id=u'AABBCCDDEEFF',
                          change_key=u'GGHHIIJJKKLLMM',
                          subject=u'нyвrιd ѕolαr eclιpѕe',
                          location=u'söüth päċïfïċ (40.1°S 123.7°W)',
                          start=datetime(year=2050, month=5, day=20, hour=20, minute=42, second=50),
                          end=datetime(year=2050, month=5, day=20, hour=21, minute=43, second=51),
                          body=u'rärr ï äm ä dïnösäür')

TEST_EVENT_UPDATED = EventFixture(id=u'AABBCCDDEEFF',
                                  change_key=u'XXXXVVV',
                                  subject=u'spärklÿ hämstër sümmër bäll',
                                  location=u'häppÿ fröġ länd',
                                  start=datetime(year=2040, month=4, day=19, hour=19, minute=41, second=49),
                                  end=datetime(year=2060, month=4, day=19, hour=20, minute=42, second=50),
                                  body=u'śő śhíńý śő véŕý śhíńý')

TEST_EVENT_MOVED = EventFixture(id=u'AABBCCDDEEFFAABBCCDDEEFF',
                          change_key=u'GGHHIIJJKKLLMMGGHHIIJJKKLLMM',
                          subject=u'нyвrιd ѕolαr eclιpѕe',
                          location=u'söüth päċïfïċ (40.1°S 123.7°W)',
                          start=datetime(year=2050, month=5, day=20, hour=20, minute=42, second=50),
                          end=datetime(year=2050, month=5, day=20, hour=21, minute=43, second=51),
                          body=u'rärr ï äm ä dïnösäür')

NOW = datetime.utcnow().replace(microsecond=0)  # If you don't remove microseconds, it screws with datetime comparisions :/

ORGANIZER = ExchangeEventOrganizer(name=u'émmý ńőéthéŕ', email=u'noether@test.linkedin.com')

# ['name', 'email', 'response', 'last_response', 'required']
PERSON_REQUIRED_ACCEPTED = ExchangeEventResponse(name=u'ämëlïä ëärhärt', email=u'earheart@test.linkedin.com', required=True, response=RESPONSE_ACCEPTED, last_response=NOW - timedelta(days=1))
PERSON_REQUIRED_TENTATIVE = ExchangeEventResponse(name=u'máŕíé ćúŕíé', email=u'curie@test.linkedin.com', required=True, response=RESPONSE_TENTATIVE, last_response=NOW - timedelta(days=2))
PERSON_REQUIRED_DECLINED = ExchangeEventResponse(name=u'ġüïlhërmïnä süġġïä', email=u'suggia@test.linkedin.com', required=True, response=RESPONSE_DECLINED, last_response=NOW - timedelta(days=3))
PERSON_REQUIRED_UNKNOWN = ExchangeEventResponse(name=u'ŕőśálíńd fŕáńklíń', email=u'franklin@test.linkedin.com', required=True, response=RESPONSE_UNKNOWN, last_response=None)

PERSON_OPTIONAL_ACCEPTED = ExchangeEventResponse(name=u'líśé méítńéŕ', email=u'meitner@test.linkedin.com', required=False, response=RESPONSE_ACCEPTED, last_response=NOW - timedelta(days=4))
PERSON_OPTIONAL_TENTATIVE = ExchangeEventResponse(name=u'αdα lovelαce', email=u'lovelace@test.linkedin.com', required=False, response=RESPONSE_TENTATIVE, last_response=NOW - timedelta(days=5))
PERSON_OPTIONAL_DECLINED = ExchangeEventResponse(name=u'ğřăčĕ ɦŏρρĕř', email=u'hopper@test.linkedin.com', required=False, response=RESPONSE_DECLINED, last_response=NOW - timedelta(days=6))
PERSON_OPTIONAL_UNKNOWN = ExchangeEventResponse(name=u'máŕgáŕét átwőőd', email=u'atwood@test.linkedin.com', required=False, response=RESPONSE_UNKNOWN, last_response=None)

SIR_NOT_APPEARING_IN_THIS_FILM = ExchangeEventResponse(name=u'sïr nöt äppëärïnġ ïn thïs fïlm', email=u'sirnotappearinginthisfilm@test.linkedin.com', required=True, response=RESPONSE_UNKNOWN, last_response=None)
SIR_ROBIN = ExchangeEventResponse(name=u'Sir Robin', email=u'sirrobin@test.linkedin.com', required=True, response=RESPONSE_UNKNOWN, last_response=None)

PERSON_WITH_NO_EMAIL_ADDRESS = ExchangeEventResponse(name=u'I am bad', email=None, required=True, response=RESPONSE_UNKNOWN, last_response=None)

REQUIRED_PEOPLE = [PERSON_REQUIRED_ACCEPTED, PERSON_REQUIRED_TENTATIVE, PERSON_REQUIRED_DECLINED, PERSON_REQUIRED_UNKNOWN]
OPTIONAL_PEOPLE = [PERSON_OPTIONAL_ACCEPTED, PERSON_OPTIONAL_TENTATIVE, PERSON_OPTIONAL_DECLINED, PERSON_OPTIONAL_UNKNOWN]
ATTENDEE_LIST = REQUIRED_PEOPLE + OPTIONAL_PEOPLE


RESOURCE = ExchangeEventResponse(name=u'flÿïnġ dïnösäür', email=u'dinosaur@test.linkedin.com', required=True, response=RESPONSE_ACCEPTED, last_response=NOW - timedelta(days=7))
UPDATED_RESOURCE = ExchangeEventResponse(name=u'ɱăğĭč čăřρĕt', email=u'carpet@test.linkedin.com', required=True, response=RESPONSE_ACCEPTED, last_response=NOW - timedelta(days=1))

RESOURCE_WITH_NO_EMAIL_ADDRESS = ExchangeEventResponse(name=u'I am also bad', email=None, required=True, response=RESPONSE_UNKNOWN, last_response=None)

GET_ITEM_RESPONSE = u"""<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Header>
    <h:ServerVersionInfo xmlns:h="http://schemas.microsoft.com/exchange/services/2006/types" xmlns="http://schemas.microsoft.com/exchange/services/2006/types" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" MajorVersion="14" MinorVersion="2" MajorBuildNumber="328" MinorBuildNumber="11"/>
  </s:Header>
  <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    <m:GetItemResponse xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages" xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types">
      <m:ResponseMessages>
        <m:GetItemResponseMessage ResponseClass="Success">
          <m:ResponseCode>NoError</m:ResponseCode>
          <m:Items>
            <t:CalendarItem>
              <t:ItemId Id="{event.id}" ChangeKey="{event.change_key}"/>
              <t:ParentFolderId Id="fooo" ChangeKey="bar"/>
              <t:ItemClass>IPM.Appointment</t:ItemClass>
              <t:Subject>{event.subject}</t:Subject>
              <t:Sensitivity>Normal</t:Sensitivity>
              <t:Body BodyType="HTML">{event.body}</t:Body>
              <t:Body BodyType="Text">{event.body}</t:Body>
              <t:DateTimeReceived>{event.start:%Y-%m-%dT%H:%M:%SZ}</t:DateTimeReceived>
              <t:Size>1935</t:Size>
              <t:Importance>Normal</t:Importance>
              <t:IsSubmitted>false</t:IsSubmitted>
              <t:IsDraft>false</t:IsDraft>
              <t:IsFromMe>false</t:IsFromMe>
              <t:IsResend>false</t:IsResend>
              <t:IsUnmodified>false</t:IsUnmodified>
              <t:DateTimeSent>{event.start:%Y-%m-%dT%H:%M:%SZ}</t:DateTimeSent>
              <t:DateTimeCreated>{event.start:%Y-%m-%dT%H:%M:%SZ}</t:DateTimeCreated>
              <t:ResponseObjects>
                <t:CancelCalendarItem/>
                <t:ForwardItem/>
              </t:ResponseObjects>
              <t:ReminderDueBy>{event.start:%Y-%m-%dT%H:%M:%SZ}</t:ReminderDueBy>
              <t:ReminderIsSet>true</t:ReminderIsSet>
              <t:ReminderMinutesBeforeStart>15</t:ReminderMinutesBeforeStart>
              <t:DisplayCc/>
              <t:DisplayTo/>
              <t:HasAttachments>false</t:HasAttachments>
              <t:Culture>en-US</t:Culture>
              <t:Start>{event.start:%Y-%m-%dT%H:%M:%SZ}</t:Start>
              <t:End>{event.end:%Y-%m-%dT%H:%M:%SZ}</t:End>
              <t:IsAllDayEvent>false</t:IsAllDayEvent>
              <t:LegacyFreeBusyStatus>Busy</t:LegacyFreeBusyStatus>
              <t:Location>{event.location}</t:Location>
              <t:IsMeeting>true</t:IsMeeting>
              <t:IsCancelled>false</t:IsCancelled>
              <t:IsRecurring>false</t:IsRecurring>
              <t:MeetingRequestWasSent>false</t:MeetingRequestWasSent>
              <t:IsResponseRequested>true</t:IsResponseRequested>
              <t:CalendarItemType>Single</t:CalendarItemType>
              <t:MyResponseType>Organizer</t:MyResponseType>
              <t:Organizer>
                <t:Mailbox>
                  <t:Name>{organizer.name}</t:Name>
                  <t:EmailAddress>{organizer.email}</t:EmailAddress>
                  <t:RoutingType>SMTP</t:RoutingType>
                </t:Mailbox>
              </t:Organizer>
              <t:RequiredAttendees>
                <t:Attendee>
                  <t:Mailbox>
                    <t:Name>{required_accepted.name}</t:Name>
                    <t:EmailAddress>{required_accepted.email}</t:EmailAddress>
                    <t:RoutingType>SMTP</t:RoutingType>
                  </t:Mailbox>
                  <t:ResponseType>{required_accepted.response}</t:ResponseType>
                  <t:LastResponseTime>{required_accepted.last_response:%Y-%m-%dT%H:%M:%SZ}</t:LastResponseTime>
                </t:Attendee>
                <t:Attendee>
                  <t:Mailbox>
                    <t:Name>{required_tentative.name}</t:Name>
                    <t:EmailAddress>{required_tentative.email}</t:EmailAddress>
                    <t:RoutingType>SMTP</t:RoutingType>
                  </t:Mailbox>
                  <t:ResponseType>{required_tentative.response}</t:ResponseType>
                  <t:LastResponseTime>{required_tentative.last_response:%Y-%m-%dT%H:%M:%SZ}</t:LastResponseTime>
                </t:Attendee>
               <t:Attendee>
                  <t:Mailbox>
                    <t:Name>{required_declined.name}</t:Name>
                    <t:EmailAddress>{required_declined.email}</t:EmailAddress>
                    <t:RoutingType>SMTP</t:RoutingType>
                  </t:Mailbox>
                  <t:ResponseType>{required_declined.response}</t:ResponseType>
                  <t:LastResponseTime>{required_declined.last_response:%Y-%m-%dT%H:%M:%SZ}</t:LastResponseTime>
                </t:Attendee>
                <t:Attendee>
                  <t:Mailbox>
                    <t:Name>{required_unknown.name}</t:Name>
                    <t:EmailAddress>{required_unknown.email}</t:EmailAddress>
                    <t:RoutingType>SMTP</t:RoutingType>
                  </t:Mailbox>
                  <t:ResponseType>{required_unknown.response}</t:ResponseType>
                </t:Attendee>
              </t:RequiredAttendees>
              <t:OptionalAttendees>
                <t:Attendee>
                  <t:Mailbox>
                    <t:Name>{optional_accepted.name}</t:Name>
                    <t:EmailAddress>{optional_accepted.email}</t:EmailAddress>
                    <t:RoutingType>SMTP</t:RoutingType>
                  </t:Mailbox>
                  <t:ResponseType>{optional_accepted.response}</t:ResponseType>
                  <t:LastResponseTime>{optional_accepted.last_response:%Y-%m-%dT%H:%M:%SZ}</t:LastResponseTime>
                </t:Attendee>
                <t:Attendee>
                  <t:Mailbox>
                    <t:Name>{optional_tentative.name}</t:Name>
                    <t:EmailAddress>{optional_tentative.email}</t:EmailAddress>
                    <t:RoutingType>SMTP</t:RoutingType>
                  </t:Mailbox>
                  <t:ResponseType>{optional_tentative.response}</t:ResponseType>
                  <t:LastResponseTime>{optional_tentative.last_response:%Y-%m-%dT%H:%M:%SZ}</t:LastResponseTime>
                </t:Attendee>
               <t:Attendee>
                  <t:Mailbox>
                    <t:Name>{optional_declined.name}</t:Name>
                    <t:EmailAddress>{optional_declined.email}</t:EmailAddress>
                    <t:RoutingType>SMTP</t:RoutingType>
                  </t:Mailbox>
                  <t:ResponseType>{optional_declined.response}</t:ResponseType>
                  <t:LastResponseTime>{optional_declined.last_response:%Y-%m-%dT%H:%M:%SZ}</t:LastResponseTime>
                </t:Attendee>
                <t:Attendee>
                  <t:Mailbox>
                    <t:Name>{optional_unknown.name}</t:Name>
                    <t:EmailAddress>{optional_unknown.email}</t:EmailAddress>
                    <t:RoutingType>SMTP</t:RoutingType>
                  </t:Mailbox>
                  <t:ResponseType>{optional_unknown.response}</t:ResponseType>
                </t:Attendee>
              </t:OptionalAttendees>
              <t:Resources>
                <t:Attendee>
                  <t:Mailbox>
                    <t:Name>{resource.name}</t:Name>
                    <t:EmailAddress>{resource.email}</t:EmailAddress>
                    <t:RoutingType>SMTP</t:RoutingType>
                  </t:Mailbox>
                  <t:ResponseType>{resource.response}</t:ResponseType>
                  <t:LastResponseTime>{resource.last_response:%Y-%m-%dT%H:%M:%SZ}</t:LastResponseTime>
                </t:Attendee>
              </t:Resources>

              <t:ConflictingMeetingCount>1</t:ConflictingMeetingCount>
              <t:AdjacentMeetingCount>1</t:AdjacentMeetingCount>
              <t:ConflictingMeetings>
                <t:CalendarItem>
                  <t:ItemId Id="rarrrrr" ChangeKey="blarg"/>
                  <t:Subject>My other awesome event</t:Subject>
                  <t:Start>{event.start:%Y-%m-%dT%H:%M:%SZ}</t:Start>
                  <t:End>{event.end:%Y-%m-%dT%H:%M:%SZ}</t:End>
                  <t:LegacyFreeBusyStatus>Busy</t:LegacyFreeBusyStatus>
                  <t:Location>Nowhere special</t:Location>
                </t:CalendarItem>
              </t:ConflictingMeetings>
              <t:AdjacentMeetings>
                <t:CalendarItem>
                  <t:ItemId Id="dinosaur" ChangeKey="goesrarrr"/>
                  <t:Subject>my other OTHER awesome event</t:Subject>
                  <t:Start>{event.start:%Y-%m-%dT%H:%M:%SZ}</t:Start>
                  <t:End>{event.end:%Y-%m-%dT%H:%M:%SZ}</t:End>
                  <t:LegacyFreeBusyStatus>Busy</t:LegacyFreeBusyStatus>
                  <t:Location>Outside</t:Location>
                </t:CalendarItem>
              </t:AdjacentMeetings>
              <t:Duration>PT1H</t:Duration>
              <t:TimeZone>(UTC-08:00) Pacific Time (US &amp; Canada)</t:TimeZone>
              <t:AppointmentSequenceNumber>0</t:AppointmentSequenceNumber>
              <t:AppointmentState>1</t:AppointmentState>
            </t:CalendarItem>
          </m:Items>
        </m:GetItemResponseMessage>
      </m:ResponseMessages>
    </m:GetItemResponse>
  </s:Body>
</s:Envelope>
""".format(event=TEST_EVENT,
           organizer=ORGANIZER,
           required_accepted=PERSON_REQUIRED_ACCEPTED,
           required_tentative=PERSON_REQUIRED_TENTATIVE,
           required_declined=PERSON_REQUIRED_DECLINED,
           required_unknown=PERSON_REQUIRED_UNKNOWN,
           optional_accepted=PERSON_OPTIONAL_ACCEPTED,
           optional_tentative=PERSON_OPTIONAL_TENTATIVE,
           optional_declined=PERSON_OPTIONAL_DECLINED,
           optional_unknown=PERSON_OPTIONAL_UNKNOWN,
           resource=RESOURCE
           )

GET_ITEM_RESPONSE_ID_ONLY = u"""<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <soap:Header>
    <t:ServerVersionInfo MajorVersion="8" MinorVersion="0" MajorBuildNumber="602" MinorBuildNumber="0"
                       xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"/>
  </soap:Header>
  <soap:Body>
    <GetItemResponse xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages"
                   xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
                   xmlns="http://schemas.microsoft.com/exchange/services/2006/messages">
      <m:ResponseMessages>
        <m:GetItemResponseMessage ResponseClass="Success">
          <m:ResponseCode>NoError</m:ResponseCode>
          <m:Items>
            <t:CalendarItem>
              <t:ItemId Id="{event.id}" ChangeKey="{event.change_key}"/>
            </t:CalendarItem>
          </m:Items>
        </m:GetItemResponseMessage>
      </m:ResponseMessages>
    </GetItemResponse>
  </soap:Body>
</soap:Envelope>""".format(event=TEST_EVENT)


ITEM_DOES_NOT_EXIST = u"""<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Header>
    <h:ServerVersionInfo xmlns:h="http://schemas.microsoft.com/exchange/services/2006/types" xmlns="http://schemas.microsoft.com/exchange/services/2006/types" xmlns:xsi="http://www.w3.org/2001/XMLSchem\
a-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" MajorVersion="14" MinorVersion="2" MajorBuildNumber="328" MinorBuildNumber="11"/>
  </s:Header>
  <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    <m:GetItemResponse xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages" xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types">
      <m:ResponseMessages>
        <m:GetItemResponseMessage ResponseClass="Error">
          <m:MessageText>The specified object was not found in the store.</m:MessageText>
          <m:ResponseCode>ErrorItemNotFound</m:ResponseCode>
          <m:DescriptiveLinkKey>0</m:DescriptiveLinkKey>
          <m:Items/>
        </m:GetItemResponseMessage>
      </m:ResponseMessages>
    </m:GetItemResponse>
  </s:Body>
</s:Envelope>"""

SOAP_FAULT = u"""<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <s:Fault>
      <faultcode xmlns:a="http://schemas.microsoft.com/exchange/services/2006/types">a:ErrorSchemaValidation</faultcode>
      <faultstring xml:lang="en-US">The request failed schema validation: Could not find schema information for the element 'bad'.</faultstring>
      <detail>
        <e:ResponseCode xmlns:e="http://schemas.microsoft.com/exchange/services/2006/errors">ErrorSchemaValidation</e:ResponseCode>
        <e:Message xmlns:e="http://schemas.microsoft.com/exchange/services/2006/errors">The request failed schema validation.</e:Message>
        <t:MessageXml xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types">
          <t:LineNumber>11</t:LineNumber>
          <t:LinePosition>14</t:LinePosition>
          <t:Violation>Could not find schema information for the element 'boguselement'.</t:Violation>
        </t:MessageXml>
      </detail>
    </s:Fault>
  </s:Body>
</s:Envelope>"""


DELETE_ITEM_RESPONSE = u"""<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <soap:Header>
    <t:ServerVersionInfo MajorVersion="8" MinorVersion="0" MajorBuildNumber="595" MinorBuildNumber="0"
                         xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types" />
  </soap:Header>
  <soap:Body>
    <DeleteItemResponse xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages"
                        xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
                        xmlns="http://schemas.microsoft.com/exchange/services/2006/messages">
      <m:ResponseMessages>
        <m:DeleteItemResponseMessage ResponseClass="Success">
          <m:ResponseCode>NoError</m:ResponseCode>
        </m:DeleteItemResponseMessage>
      </m:ResponseMessages>
    </DeleteItemResponse>
  </soap:Body>
</soap:Envelope>"""


CREATE_ITEM_RESPONSE = u"""<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <soap:Header>
    <t:ServerVersionInfo MajorVersion="8" MinorVersion="0" MajorBuildNumber="685" MinorBuildNumber="8"
                         xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types" />
  </soap:Header>
  <soap:Body>
    <CreateItemResponse xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages"
                        xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
                        xmlns="http://schemas.microsoft.com/exchange/services/2006/messages">
      <m:ResponseMessages>
        <m:CreateItemResponseMessage ResponseClass="Success">
          <m:ResponseCode>NoError</m:ResponseCode>
          <m:Items>
            <t:CalendarItem>
              <t:ItemId Id="{event.id}" ChangeKey="{event.change_key}" />
            </t:CalendarItem>
          </m:Items>
        </m:CreateItemResponseMessage>
      </m:ResponseMessages>
    </CreateItemResponse>
  </soap:Body>
</soap:Envelope>""".format(event=TEST_EVENT)


UPDATE_ITEM_RESPONSE = u"""<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <soap:Header>
    <t:ServerVersionInfo MajorVersion="8" MinorVersion="0" MajorBuildNumber="664" MinorBuildNumber="0"
                         xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"/>
  </soap:Header>
  <soap:Body>
    <UpdateItemResponse xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages"
                        xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
      xmlns="http://schemas.microsoft.com/exchange/services/2006/messages">
      <m:ResponseMessages>
        <m:UpdateItemResponseMessage ResponseClass="Success">
          <m:ResponseCode>NoError</m:ResponseCode>
          <m:Items>
            <t:Message>
              <t:ItemId Id="{event.id}" ChangeKey="{event.change_key}" />
            </t:Message>
          </m:Items>
        </m:UpdateItemResponseMessage>
      </m:ResponseMessages>
    </UpdateItemResponse>
  </soap:Body>
</soap:Envelope>""".format(event=TEST_EVENT)


GET_FOLDER_RESPONSE = u"""<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <soap:Header>
    <t:ServerVersionInfo MajorVersion="8" MinorVersion="0" MajorBuildNumber="628" MinorBuildNumber="0"
                         xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types" />
  </soap:Header>
  <soap:Body>
    <GetFolderResponse xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages"
                       xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
                       xmlns="http://schemas.microsoft.com/exchange/services/2006/messages">
      <m:ResponseMessages>
        <m:GetFolderResponseMessage ResponseClass="Success">
          <m:ResponseCode>NoError</m:ResponseCode>
          <m:Folders>
            <t:{folder.folder_type}>
              <t:FolderId Id="{folder.id}" ChangeKey="{folder.change_key}" />
              <t:ParentFolderId Id="{folder.parent_id}" ChangeKey="AQAAAA=="/>
              <t:DisplayName>{folder.display_name}</t:DisplayName>
              <t:TotalCount>2</t:TotalCount>
              <t:ChildFolderCount>0</t:ChildFolderCount>
              <t:UnreadCount>2</t:UnreadCount>
            </t:{folder.folder_type}>
          </m:Folders>
        </m:GetFolderResponseMessage>
      </m:ResponseMessages>
    </GetFolderResponse>
  </soap:Body>
</soap:Envelope>""".format(folder=TEST_FOLDER)


FOLDER_DOES_NOT_EXIST = u"""<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Header>
    <h:ServerVersionInfo xmlns:h="http://schemas.microsoft.com/exchange/services/2006/types"
                         xmlns="http://schemas.microsoft.com/exchange/services/2006/types"
                         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                         xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                         MajorVersion="14"
                         MinorVersion="3"
                         MajorBuildNumber="181"
                         MinorBuildNumber="6"/>
  </s:Header>
  <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    <m:GetFolderResponse xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages"
                         xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types">
      <m:ResponseMessages>
        <m:GetFolderResponseMessage ResponseClass="Error">
          <m:MessageText>The specified object was not found in the store.</m:MessageText>
          <m:ResponseCode>ErrorItemNotFound</m:ResponseCode>
          <m:DescriptiveLinkKey>0</m:DescriptiveLinkKey>
          <m:Folders/>
        </m:GetFolderResponseMessage>
      </m:ResponseMessages>
    </m:GetFolderResponse>
  </s:Body>
</s:Envelope>"""


CREATE_FOLDER_RESPONSE = u"""<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Header>
    <h:ServerVersionInfo xmlns:h="http://schemas.microsoft.com/exchange/services/2006/types"
                         xmlns="http://schemas.microsoft.com/exchange/services/2006/types"
                         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                         xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                         MajorVersion="14"
                         MinorVersion="3"
                         MajorBuildNumber="181"
                         MinorBuildNumber="6"/>
  </s:Header>
  <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    <m:CreateFolderResponse xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages"
                            xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types">
      <m:ResponseMessages>
        <m:CreateFolderResponseMessage ResponseClass="Success">
          <m:ResponseCode>NoError</m:ResponseCode>
          <m:Folders>
            <t:{folder.folder_type}>
              <t:FolderId Id="{folder.id}" ChangeKey="{folder.change_key}"/>
            </t:{folder.folder_type}>
          </m:Folders>
        </m:CreateFolderResponseMessage>
      </m:ResponseMessages>
    </m:CreateFolderResponse>
  </s:Body>
</s:Envelope>""".format(folder=TEST_FOLDER)


DELETE_FOLDER_RESPONSE = u"""<?xml version="1.0" encoding="utf-8" ?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <soap:Header>
    <t:ServerVersionInfo MajorVersion="8" MinorVersion="0" MajorBuildNumber="595" MinorBuildNumber="0"
                         xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types" />
  </soap:Header>
  <soap:Body>
    <DeleteFolderResponse xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages"
                          xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
                          xmlns="http://schemas.microsoft.com/exchange/services/2006/messages">
      <m:ResponseMessages>
        <m:DeleteFolderResponseMessage ResponseClass="Success">
          <m:ResponseCode>NoError</m:ResponseCode>
        </m:DeleteFolderResponseMessage>
      </m:ResponseMessages>
    </DeleteFolderResponse>
  </soap:Body>
</soap:Envelope>"""


FIND_FOLDER_RESPONSE = u"""<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Header>
    <h:ServerVersionInfo xmlns:h="http://schemas.microsoft.com/exchange/services/2006/types"
                         xmlns="http://schemas.microsoft.com/exchange/services/2006/types"
                         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                         xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                         MajorVersion="14" MinorVersion="3" MajorBuildNumber="181" MinorBuildNumber="6"/>
  </s:Header>
  <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    <m:FindFolderResponse xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages"
                          xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types">
      <m:ResponseMessages>
        <m:FindFolderResponseMessage ResponseClass="Success">
          <m:ResponseCode>NoError</m:ResponseCode>
          <m:RootFolder TotalItemsInView="4" IncludesLastItemInRange="true">
            <t:Folders>
              <t:Folder>
                <t:FolderId Id="AAhKNOZAAA=" ChangeKey="AhKNOb"/>
                <t:ParentFolderId Id="AABBCCDDEEFF" ChangeKey="AQAAAA=="/>
                <t:DisplayName>classrooms</t:DisplayName>
                <t:TotalCount>0</t:TotalCount>
                <t:ChildFolderCount>1</t:ChildFolderCount>
                <t:UnreadCount>0</t:UnreadCount>
              </t:Folder>
              <t:CalendarFolder>
                <t:FolderId Id="AhKSe7AAA=" ChangeKey="uAhKSe9"/>
                <t:ParentFolderId Id="AABBCCDDEEFF" ChangeKey="AQAAAA=="/>
                <t:FolderClass>IPF.Appointment</t:FolderClass>
                <t:DisplayName>conference</t:DisplayName>
                <t:TotalCount>0</t:TotalCount>
                <t:ChildFolderCount>0</t:ChildFolderCount>
              </t:CalendarFolder>
              <t:CalendarFolder>
                <t:FolderId Id="AAhKSrHAAA=" ChangeKey="AhKSrJ"/>
                <t:ParentFolderId Id="AABBCCDDEEFF" ChangeKey="AQAAAA=="/>
                <t:FolderClass>IPF.Appointment</t:FolderClass>
                <t:DisplayName>conference0</t:DisplayName>
                <t:TotalCount>0</t:TotalCount>
                <t:ChildFolderCount>0</t:ChildFolderCount>
              </t:CalendarFolder>
              <t:CalendarFolder>
                <t:FolderId Id="AAhKSw+AAA=" ChangeKey="AhKSxA"/>
                <t:ParentFolderId Id="AABBCCDDEEFF" ChangeKey="AQAAAA=="/>
                <t:FolderClass>IPF.Appointment</t:FolderClass>
                <t:DisplayName>conference1</t:DisplayName>
                <t:TotalCount>0</t:TotalCount>
                <t:ChildFolderCount>0</t:ChildFolderCount>
              </t:CalendarFolder>
            </t:Folders>
          </m:RootFolder>
        </m:FindFolderResponseMessage>
      </m:ResponseMessages>
    </m:FindFolderResponse>
  </s:Body>
</s:Envelope>"""


MOVE_EVENT_RESPONSE = u"""<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Header>
    <h:ServerVersionInfo xmlns:h="http://schemas.microsoft.com/exchange/services/2006/types"
                         xmlns="http://schemas.microsoft.com/exchange/services/2006/types"
                         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                         xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                         MajorVersion="14" MinorVersion="3" MajorBuildNumber="181" MinorBuildNumber="6"/>
  </s:Header>
  <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    <m:MoveItemResponse xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages"
                        xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types">
      <m:ResponseMessages>
        <m:MoveItemResponseMessage ResponseClass="Success">
          <m:ResponseCode>NoError</m:ResponseCode>
          <m:Items>
            <t:CalendarItem>
              <t:ItemId Id="{event.id}" ChangeKey="{event.change_key}"/>
            </t:CalendarItem>
          </m:Items>
        </m:MoveItemResponseMessage>
      </m:ResponseMessages>
    </m:MoveItemResponse>
  </s:Body>
</s:Envelope>""".format(event=TEST_EVENT_MOVED)


MOVE_FOLDER_RESPONSE = u"""<?xml version="1.0" encoding="utf-8" ?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <soap:Header>
    <t:ServerVersionInfo MajorVersion="8" MinorVersion="0" MajorBuildNumber="685" MinorBuildNumber="8"
                         xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types" />
  </soap:Header>
  <soap:Body>
    <MoveFolderResponse xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages"
                        xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
                        xmlns="http://schemas.microsoft.com/exchange/services/2006/messages">
      <m:ResponseMessages>
        <m:MoveFolderResponseMessage ResponseClass="Success">
          <m:ResponseCode>NoError</m:ResponseCode>
          <m:Folders>
            <t:Folder>
              <t:FolderId Id="{folder.id}" ChangeKey="folder.change_key" />
            </t:Folder>
          </m:Folders>
        </m:MoveFolderResponseMessage>
      </m:ResponseMessages>
    </MoveFolderResponse>
  </soap:Body>
</soap:Envelope>""".format(folder=TEST_FOLDER)
