#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# File: jabber.py

import sleekxmpp
import logging
from notifierlib.notifierlib import Channel

__author__ = '''Costas Tyfoxylos <costas.tyf@gmail.com>, Argiris Gounaris <agounaris@gmail.com>'''
__docformat__ = 'plaintext'
__date__ = '''19-09-2017'''


class XmppClient(sleekxmpp.ClientXMPP):
    """A basic SleekXMPP bot, logs in, sends message, logs out."""

    def __init__(self,
                 user_id,
                 password,
                 recipient,
                 message,
                 server,
                 port,
                 tls=False,
                 ssl=True,
                 reattempt=False):
        super(XmppClient, self).__init__(user_id, password)
        self._logger = logging.getLogger(self.__class__.__name__)
        self.recipient = recipient
        self.message = message
        self.server = server
        self.port = port
        self.tls = tls
        self.ssl = ssl
        self.reattempt = reattempt
        self.add_event_handler('session_start', self.start)
        self.register_plugin('xep_0030')  # Service Discovery
        self.register_plugin('xep_0199')  # XMPP Ping
        # Connect to the XMPP server and start processing XMPP stanzas.
        if not self.connect((self.server, self.port),
                            use_tls=self.tls,
                            use_ssl=self.ssl,
                            reattempt=self.reattempt):
            message = ('Could not connect to '
                       '{server}:{port}').format(server=self.server,
                                                 port=self.port)
            self._logger.error(message)
            raise SyntaxError(message)
        self.process(block=True)

    def start(self, event):
        _ = event
        self.send_message(mto=self.recipient,
                          mbody=self.message,
                          mtype='chat')
        self.disconnect(wait=True)


class XmppGroupClient(sleekxmpp.ClientXMPP):
    """A basic SleekXMPP bot, logs in, sends message, logs out."""

    def __init__(self,
                 user_id,
                 password,
                 room,
                 nickname,
                 message,
                 server,
                 port,
                 room_password=None,
                 tls=False,
                 ssl=True,
                 reattempt=False):
        super(XmppGroupClient, self).__init__(user_id, password)
        self._logger = logging.getLogger(self.__class__.__name__)
        self.room = room
        self.room_password = room_password
        self.nickname = nickname
        self.message = message
        self.server = server
        self.port = port
        self.tls = tls
        self.ssl = ssl
        self.reattempt = reattempt
        self.add_event_handler('session_start', self.start)
        self.register_plugin('xep_0030')  # Service Discovery
        self.register_plugin('xep_0045')  # Multi-User Chat
        self.register_plugin('xep_0199')  # XMPP Ping
        # Connect to the XMPP server and start processing XMPP stanzas.
        if not self.connect((self.server, self.port),
                            use_tls=self.tls,
                            use_ssl=self.ssl,
                            reattempt=self.reattempt):
            message = ('Could not connect to '
                       '{server}:{port}').format(server=self.server,
                                                 port=self.port)
            self._logger.error(message)
            raise SyntaxError(message)
        self.process(block=True)

    def start(self, event):
        _ = event
        self.plugin['xep_0045'].joinMUC(self.room,
                                        self.nickname,
                                        # If a room password is needed, use:
                                        password=self.room_password,
                                        wait=True)
        self.send_message(mto=self.room,
                          mbody=self.message,
                          mtype='groupchat')
        self.disconnect(wait=True)


class Jabber(Channel):

    def __init__(self,
                 name,
                 user_id,
                 password,
                 recipient_id,
                 server,
                 port,
                 tls=False,
                 ssl=True,
                 reattempt=False):
        super(Jabber, self).__init__()
        self.name = name
        self.user = user_id
        self.password = password
        self.server = server
        self.recipient = recipient_id
        self.port = port
        self.tls = tls
        self.ssl = ssl
        self.reattempt = reattempt

    def notify(self, **kwargs):
        message = kwargs.get('message')
        _ = XmppClient(self.user,
                       self.password,
                       self.recipient,
                       message,
                       self.server,
                       self.port,
                       self.tls,
                       self.ssl,
                       self.reattempt)
        return True


class JabberGroup(Channel):
    def __init__(self,
                 name,
                 user_id,
                 password,
                 room,
                 nickname,
                 server,
                 port,
                 room_password=None,
                 tls=False,
                 ssl=True,
                 reattempt=False):
        super(JabberGroup, self).__init__()
        self.name = name
        self.user = user_id
        self.password = password
        self.nickname = nickname
        self.room = room
        self.room_password = room_password
        self.server = server
        self.port = port
        self.tls = tls
        self.ssl = ssl
        self.reattempt = reattempt

    def notify(self, **kwargs):
        message = kwargs.get('message')
        _ = XmppGroupClient(self.user,
                            self.password,
                            self.room,
                            self.nickname,
                            message,
                            self.server,
                            self.port,
                            self.room_password,
                            self.tls,
                            self.ssl,
                            self.reattempt)
        return True
