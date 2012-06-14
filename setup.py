#!/usr/bin/env python

# Copyright (c) 2003-2009 Ralph Meijer
# See LICENSE for details.

from setuptools import setup

setup(name='ircjabberrelay',
      version='0.0.1',
      description='Relay between IRC and Jabber',
      author='Alexey Torkhov',
      author_email='atorkhov@gmail.com',
      maintainer_email='atorkhov@gmail.com',
      url='https://github.com/atorkhov/ircjabberrelay',
      license='Public Domain',
      platforms='any',
      packages=['ircjabberrelay'],
      data_files=[
            ('/usr/bin', ['ircjabberrelay.tac']),
            ('/etc/ircjabberrelay', ['ignore'])
      ]
)
