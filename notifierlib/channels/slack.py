#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# File: slack.py
"""Slack module file"""

import requests
from notifierlib.notifierlib import Channel
from jinja2 import Environment

__author__ = '''Oriol Fabregas <fabregas.oriol@gmail.com>'''
__docformat__ = 'plaintext'
__date__ = '''20-09-2017'''


class Slack(Channel):
    """
    Integration with Slack

    In a team, a channel is public by design, therefore the attribute 'private'
    is False by default. A private channel is just a group.

    Slack API understands a channel name as "#channel" format and a group as
    "group". Also, by default will reply to the whole channel.

    "as_user" is also implemented by default in this notification.

    +info https://api.slack.com/methods/chat.postMessage#channels
    """
    def __init__(self,
                 name,
                 token,
                 channel,
                 template=None,
                 private=False,
                 reply_broadcast=False):
        super(Slack, self).__init__(name)
        self.private = private
        self.channel = channel if self.private else '#{channel}'.format(channel=channel)
        self.template = template
        self.site = 'https://slack.com/api'
        self.reply_broadcast = reply_broadcast
        self.__token = token

    def notify(self, **kwargs):
        result = True
        if self.template:
            body = Environment().from_string(self.template).render(**kwargs)
        else:
            body = kwargs.get('message')

        response = requests.post(url='{site}/auth.test'.format(site=self.site),
                                 data={'token': self.__token})
        if not response.json().get('ok'):
            message = ('Error getting user details to {url}.\n'
                       'Response: {response}\n').format(url=response.url,
                                                        response=response.content)
            self._logger.error(message)
            result = False
            return result

        arguments = {'channel': self.channel,
                     'token': self.__token,
                     'text': body,
                     'reply_broadcast': self.reply_broadcast,
                     'as_user': response.json().get('user_id')}
        response = requests.post(url='{site}/chat.postMessage'.format(site=self.site),
                                 data=arguments)
        if not response.json().get('ok'):
            self._logger.error('Error while sending message to channel {channel} \n' \
                               'Response text: {response}'.format(channel=self.channel,
                                                                  response=response.content))
            result = False

        if result:
            self._logger.debug(('Message sent successfully. Response text: '
                                '{response}').format(response=response.text))
        return result
