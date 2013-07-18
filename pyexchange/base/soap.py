"""
(c) 2013 LinkedIn Corp. All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License");?you may not use this file except in compliance with the License. You may obtain a copy of the License at  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software?distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
import logging

from lxml import etree
from datetime import datetime
from pytz import utc

from ..exceptions import FailedExchangeException

SOAP_NS = u'http://schemas.xmlsoap.org/soap/envelope/'

SOAP_NAMESPACES = {u's': SOAP_NS}

log = logging.getLogger('pyexchange')


class ExchangeServiceSOAP(object):

  EXCHANGE_DATE_FORMAT = u"%Y-%m-%dT%H:%M:%SZ"

  def __init__(self, connection):
    self.connection = connection

  def send(self, xml, headers=None, retries=4, timeout=30, encoding="utf-8"):
    request_xml = self._wrap_soap_xml_request(xml)
    log.info(etree.tostring(request_xml, encoding=encoding, pretty_print=True))
    response = self._send_soap_request(request_xml, headers=headers, retries=retries, timeout=timeout, encoding=encoding)
    return self._parse(response, encoding=encoding)

  def _parse(self, response, encoding="utf-8"):

    try:
      tree = etree.XML(response.encode(encoding))
    except (etree.XMLSyntaxError, TypeError) as err:
      raise FailedExchangeException(u"Unable to parse response from Exchange - check your login information. Error: %s" % err)

    self._check_for_errors(tree)

    log.info(etree.tostring(tree, encoding=encoding, pretty_print=True))
    return tree

  def _check_for_errors(self, xml_tree):
    self._check_for_SOAP_fault(xml_tree)

  def _check_for_SOAP_fault(self, xml_tree):
    # Check for SOAP errors. if <soap:Fault> is anywhere in the response, flip out

    fault_nodes = xml_tree.xpath(u'//s:Fault', namespaces=SOAP_NAMESPACES)

    if fault_nodes:
      fault = fault_nodes[0]
      raise FailedExchangeException(u"SOAP Fault from Exchange server", fault.text)

  def _send_soap_request(self, xml, headers=None, retries=2, timeout=30, encoding="utf-8"):
    body = etree.tostring(xml, encoding=encoding)

    response = self.connection.send(body, headers, retries, timeout)
    return response

  def _wrap_soap_xml_request(self, exchange_xml):
    root = etree.Element(u"{%s}Envelope" % SOAP_NS)
    body = etree.SubElement(root, u"{%s}Body" % SOAP_NS)
    body.append(exchange_xml)

    return root

  def _parse_date(self, date_string):
    date = datetime.strptime(date_string, self.EXCHANGE_DATE_FORMAT)
    date.replace(tzinfo=utc)

    return date

  def _xpath_to_dict(self, element, property_map, namespace_map):
    """
    property_map = {
      u'name'         : { u'xpath' : u't:Mailbox/t:Name'},
      u'email'        : { u'xpath' : u't:Mailbox/t:EmailAddress'},
      u'response'     : { u'xpath' : u't:ResponseType'},
      u'last_response': { u'xpath' : u't:LastResponseTime', u'cast': u'datetime'},
    }

    This runs the given xpath on the node and returns a dictionary

    """

    result = {}

    log.info(etree.tostring(element, pretty_print=True))

    for key in property_map:
      item = property_map[key]
      log.info(u'Pulling xpath {xpath} into key {key}'.format(key=key, xpath=item[u'xpath']))
      nodes = element.xpath(item[u'xpath'], namespaces=namespace_map)

      if nodes:
        result_for_node = []

        for node in nodes:
          cast_as = item.get(u'cast', None)

          if cast_as == u'datetime':
            result_for_node.append(self._parse_date(node.text))
          else:
            result_for_node.append(node.text)

        if not result_for_node:
          result[key] = None
        elif len(result_for_node) == 1:
          result[key] = result_for_node[0]
        else:
          result[key] = result_for_node

    return result
