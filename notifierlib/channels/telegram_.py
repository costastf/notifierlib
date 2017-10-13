#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# File: telegram_.py

import telegram
import logging
from notifierlib.notifierlib import Channel
from jinja2 import Environment as Env


__author__ = '''Costas Tyfoxylos <costas.tyf@gmail.com>'''
__docformat__ = 'plaintext'
__date__ = '''19-09-2017'''


class Telegram(Channel):
    def __init__(self, name, token, chat_id, template=None, formatting=None):
        super(Telegram, self).__init__(name)
        self.chat_id = chat_id
        self.template = template
        self.formatting = self._get_formatting(formatting)
        self._bot = telegram.Bot(token)

    @staticmethod
    def _get_formatting(formatting):
        if formatting:
            if formatting.upper() not in ['MARKDOWN', 'HTML']:
                raise ValueError('Unsupported formatting {}'.format(formatting))
            else:
                formatting = formatting.upper()
        return formatting

    def notify(self, **kwargs):
        try:
            body = Env().from_string(self.template).render(**kwargs) if \
                self.template else kwargs.get('message')
            arguments = {'chat_id': self.chat_id,
                         'text': body}
            if self.formatting:
                parse_mode = getattr(telegram.ParseMode, self.formatting)
                arguments['parse_mode'] = parse_mode
            self._bot.send_message(**arguments)
        except Exception:
            self._logger.exception()
            return False
        return True
