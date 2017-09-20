#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# File: slack.py
"""Slack module file"""

from slackclient import SlackClient
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
        self.channel = self.__determine_channel(channel)
        self.template = template
        self.reply_broadcast = reply_broadcast
        self._bot = SlackClient(token=token)

    def __determine_channel(self, channel):
        """
        Channel name for Slack API

        If 'private' is set to True, it is understood it is a Group and not a
        Channel and so it is the string.

        :param channel: string
        :return: string
        """
        if self.private:
            return channel
        else:
            return '#{channel}'.format(channel=channel)

    def notify(self, **kwargs):
        if self.template:
            body = Environment().from_string(self.template).render(**kwargs)
        else:
            body = kwargs.get('message')

        arguments = {'channel': self.channel,
                     'text': body,
                     'reply_broadcast': self.reply_broadcast,
                     'as_user': self._bot.api_call("auth.test").get('user_id')}
        self._bot.api_call("chat.postMessage", **arguments)
        return True
