#!/usr/bin/twistd -ny

from twisted.application import service
from ircjabberrelay.manager import *

application = service.Application("ircjabberrelay")

initIrcJabberRelay(application)
