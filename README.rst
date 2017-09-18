===========
notifierlib
===========

A library that implements a kind of fan-out pattern, sending messages to very different endpoints.
Extendable through the implementation of custom Channels.


* Documentation: http://notifierlib.readthedocs.io/en/latest/

Features
--------

Introduced concepts are:

* Channels
    A channel is a communication endpoint capable of sending some type of message exposing
a "notify" method.

* Groups
    A group is a construct bringing channels together under a common entrypoint showing up
as a method call of the main Notifier object.

* Notifier
    The main object bringing together channels as broadcast by default and exposing methods
to register and unregister channels and add and remove groups.

For a more detailed explanation please see the USAGE.rst file.
