#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# File: stdout.py


from notifierlib.notifierlib import Channel


__author__ = '''Costas Tyfoxylos <costas.tyf@gmail.com>'''
__docformat__ = 'plaintext'
__date__ = '''18-09-2017'''


class Stdout(Channel):
    """A simple library to print to stdout"""

    def __init__(self, name):
        self.name = name

    @staticmethod
    def _format_arguments(arguments):
        longer_string_length = len(max(arguments.keys(), key=len))
        keys = sorted(arguments.keys())
        output = []
        for entry in keys:
            width = longer_string_length + 1 - len(entry)
            text = ' '.join([word.capitalize() for word in entry.split()])
            value = arguments[entry]
            output.append('{legend:{align}{width}} :{value}'.format(legend=text,
                                                                    align='<',
                                                                    width=width,
                                                                    value=value)
                          )
        return '\n'.join(output)

    def notify(self, **kwargs):
        print(self._format_arguments(kwargs))
        return True
