#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# File: email.py
"""Email module file"""

from emaillib import EasySender
from notifierlib.notifierlib import Channel
from jinja2 import Environment

__author__ = '''Costas Tyfoxylos <costas.tyf@gmail.com>'''
__docformat__ = 'plaintext'
__date__ = '''18-09-2017'''


class Email(Channel):
    def __init__(self,
                 name,
                 sender,
                 recipient,
                 smtp_address,
                 username=None,
                 password=None,
                 tls=False,
                 ssl=True,
                 port=587,
                 template=None,
                 content='text'):
        super(Email, self).__init__(name)
        self.recipient = recipient
        self.sender = sender
        self.email = EasySender(smtp_address=smtp_address,
                                username=username,
                                password=password,
                                ssl=ssl,
                                tls=tls,
                                port=port)
        self.template = template
        self.content = content

    def notify(self, **kwargs):
        try:
            if self.template:
                body = Environment().from_string(self.template).render(**kwargs)
            else:
                body = kwargs.get('message')
            result = self.email.send(sender=self.sender,
                                     recipients=self.recipient,
                                     subject=kwargs.get('subject'),
                                     body=body,
                                     content=self.content)
            if not result:
                self._logger.error('Failed sending email')
        except Exception:
            self._logger.exception()
            return False
        return True if result else False
