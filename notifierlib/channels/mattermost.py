#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# File: mattermost.py


import logging
import requests
import json
from notifierlib.notifierlib import Channel
from jinja2 import Environment

__author__ = '''Costas Tyfoxylos <costas.tyf@gmail.com>'''
__docformat__ = 'plaintext'
__date__ = '''19-09-2017'''


class Mattermost(Channel):

    def __init__(self, name, webhook_url, template=None):
        super(Mattermost, self).__init__(name)
        self.url = webhook_url
        self.template = template

    def notify(self, **kwargs):
        try:
            if self.template:
                body = Environment().from_string(self.template).render(**kwargs)
            else:
                body = kwargs.get('message')
            headers = {'Content-Type': 'application/json'}
            payload = {'text': body}
            response = requests.post(self.url,
                                     data=json.dumps(payload),
                                     headers=headers,
                                     timeout=20)
            if not response.ok:
                message = ('Error sending message to {url}.\n'
                           'Message: {message}\n'
                           'Response: '
                           '{response}\n').format(url=self.url,
                                                  message=body,
                                                  reason=response.content)
                self._logger.error(message)
                return False
            self._logger.debug(('Message sent successfully. Response text: '
                                '{response}').format(response=response.text))
        except Exception:
            self._logger.exception()
            return False
        return True
