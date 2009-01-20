##############################################################################
#
# Copyright (c) 2003 Nexedi SARL and Contributors. All Rights Reserved.
#          Sebastien Robin <seb@nexedi.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
##############################################################################

import smtplib # to send emails
from Publication import Publication,Subscriber
from Subscription import Signature
from XMLSyncUtils import XMLSyncUtils
from Conduit.ERP5Conduit import ERP5Conduit
from Products.CMFCore.utils import getToolByName
from Products.ERP5Security.ERP5UserManager import ERP5UserManager
from Products.PluggableAuthService.interfaces.plugins import\
    IAuthenticationPlugin
from AccessControl.SecurityManagement import newSecurityManager
import commands
from DateTime import DateTime
from zLOG import LOG, DEBUG, INFO, WARNING

class PublicationSynchronization(XMLSyncUtils):
  """
    Receive the first XML message from the client
  """

  def PubSyncInit(self, publication=None, xml_client=None, subscriber=None,
      sync_type=None):
    """
      Read the client xml message
      Send the first XML message from the server
    """
    LOG('PubSyncInit', INFO, 'Starting... publication: %s' % (publication.getPath()))
    #the session id is set at the same value of those of the client
    subscriber.setSessionId(self.getSessionIdFromXml(xml_client))
    #same for the message id
    subscriber.setMessageId(self.getMessageIdFromXml(xml_client))     
    #at the begining of the synchronization the subscriber is not authenticated
    subscriber.setAuthenticated(False)
    #the last_message_id is 1 because the message that 
    #we are about to send is the message 1      
    subscriber.initLastMessageId(1)

    alert = None
    # Get informations from the body
    if xml_client is not None: # We have received a message
      last_anchor = self.getAlertLastAnchor(xml_client)
      next_anchor = self.getAlertNextAnchor(xml_client)
      alert = self.checkAlert(xml_client)
      alert_code = self.getAlertCodeFromXML(xml_client)
      cred = self.checkCred(xml_client)

      #the source and the target of the subscriber are reversed compared 
      # to those of the publication :
      subscriber.setSourceURI(self.getTargetURI(xml_client))
      subscriber.setTargetURI(self.getSourceURI(xml_client))

      xml_list = []
      xml = xml_list.append
      cmd_id = 1 # specifies a SyncML message-unique command identifier      
      xml('<SyncML>\n')
      # syncml header
      xml(self.SyncMLHeader(subscriber.getSessionId(),
        subscriber.getMessageId(),
        subscriber.getSubscriptionUrl(),
        publication.getPublicationUrl()))
      # syncml body
      xml(' <SyncBody>\n')


      #at the begining, the code is initialised at UNAUTHORIZED
      auth_code = self.UNAUTHORIZED
      if not cred:
        auth_code = self.AUTH_REQUIRED
        LOG("PubSyncInit there's no credential !!!", INFO,'')
        # Prepare the xml message for the Sync initialization package
        xml(self.SyncMLChal(cmd_id, "SyncHdr",
          publication.getPublicationUrl(), subscriber.getSubscriptionUrl(),
          publication.getAuthenticationFormat(),
          publication.getAuthenticationType(), auth_code))
        cmd_id += 1
        # chal message
        xml_status, cmd_id = self.SyncMLStatus(
                                      xml_client,
                                      auth_code,
                                      cmd_id,
                                      next_anchor,
                                      subscription=subscriber).values()
        xml(xml_status)
      else:
        # If slow sync, then resend everything
        if alert_code == self.SLOW_SYNC and \
          subscriber.getNextAnchor() != self.NULL_ANCHOR:
          LOG('Warning !!!, reseting client synchronization for subscriber:', WARNING,
              subscriber.getPath())
          subscriber.resetAllSignatures()
          subscriber.resetAnchors()
  
        # Check if the last time synchronization is the same as the client one
        if subscriber.getNextAnchor() != last_anchor:
          if last_anchor in (None, ''):
            LOG('PubSyncInit', INFO, 'anchor null')
          else:
            mess = '\nsubscriber.getNextAnchor:\t%s\nsubscriber.getLastAnchor:\t%s\
                  \nlast_anchor:\t\t\t%s\nnext_anchor:\t\t\t%s' % \
                  (subscriber.getNextAnchor(),
                    subscriber.getLastAnchor(),
                    last_anchor,
                    next_anchor)
            LOG('PubSyncInit Anchors', INFO, mess)
        else:
          subscriber.setNextAnchor(next_anchor)
        (authentication_format, authentication_type, data) = \
            self.getCred(xml_client)
        if authentication_type == publication.getAuthenticationType():
          authentication_format = publication.getAuthenticationFormat()
          decoded = subscriber.decode(authentication_format, data)
          if decoded and ':' in decoded:
            (login, password) = decoded.split(':')
            uf = self.getPortalObject().acl_users
            for plugin_name, plugin in uf._getOb('plugins').listPlugins(
                                      IAuthenticationPlugin ):
              if plugin.authenticateCredentials(
                        {'login':login, 'password':password}) is not None:
                subscriber.setAuthenticated(True)
                auth_code = self.AUTH_ACCEPTED
                LOG("PubSyncInit Authentication Accepted", INFO, '')
                #here we must log in with the user authenticated :
                user = uf.getUserById(login).__of__(uf)
                newSecurityManager(None, user)
                subscriber.setUser(login)
                break
              else:
                LOG("PubSyncInit Authentication Failed !! with login :", INFO, login)
                auth_code = self.UNAUTHORIZED
        #in all others cases, the auth_code is set to UNAUTHORIZED

        # Prepare the xml message for the Sync initialization package
        if auth_code == self.AUTH_ACCEPTED:
          xml_status, cmd_id = self.SyncMLStatus(xml_client, auth_code,
              cmd_id, next_anchor, subscription=subscriber).values()
          xml(xml_status)
          # alert message
          xml(self.SyncMLAlert(cmd_id, sync_type, subscriber.getTargetURI(),
            subscriber.getSourceURI(), subscriber.getLastAnchor(),
            next_anchor))
          cmd_id += 1
        else:
          # chal message
          xml(self.SyncMLChal(cmd_id, "SyncHdr",
            publication.getPublicationUrl(), subscriber.getSubscriptionUrl(),
            publication.getAuthenticationFormat(),
            publication.getAuthenticationType(), auth_code))
          cmd_id += 1
          xml_status, cmd_id = self.SyncMLStatus(xml_client,
              self.AUTH_REQUIRED, cmd_id, next_anchor,
              subscription=subscriber).values()
          xml(xml_status)

      # We have to set every object as NOT_SYNCHRONIZED
      subscriber.startSynchronization()
    else:
      # We have started the sync from the server (may be for a conflict 
      # resolution)
      raise ValueError, "the syncml message is None. Maybe a synchronisation \
          has been started from the server (forbiden)"
      # a synchronisation is always starded from a client and can't be from
      # a server !

    xml('  <Final/>\n')
    xml(' </SyncBody>\n')
    xml('</SyncML>\n')
    xml_a = ''.join(xml_list)
    if publication.getSyncContentType() == self.CONTENT_TYPE['SYNCML_WBXML']:
      xml_a = self.xml2wbxml(xml_a)
    self.sendResponse(from_url=publication.getPublicationUrl(),
      to_url=subscriber.getSubscriptionUrl(), sync_id=publication.getTitle(),
      xml=xml_a, domain=publication,
      content_type=publication.getSyncContentType())

    return {'has_response':1, 'xml':xml_a}

  def PubSyncModif(self, publication, xml_client):
    """
    The modidification message for the publication
    """
    return self.SyncModif(publication, xml_client)
