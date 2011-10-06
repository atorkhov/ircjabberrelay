#!/usr/bin/env PYTHONPATH=.:wokkel twistd -n -y

import sys
from twisted.application import internet, service
from twisted.internet import reactor
from twisted.python import log
from twisted.words.protocols.jabber import jid
from wokkel.client import XMPPClient

from ircbot import *
from jabberbot import *

#def gotProtocol(p):
#    log.msg("Got protocol")
#    ircbot = p
#    reactor.callLater(20, sendIRC, "Ready")
#    reactor.callLater(20, sendJabber, "Ready")
##    p.sendMessage("Hello")
##    reactor.callLater(1, p.sendMessage, "This is sent in a second")
##    reactor.callLater(2, p.transport.loseConnection)

class RelayManager:
    def __init__(self):
        self.ircbot = None
        self.jabberbot = None

    def setIRC(self, ircbot):
        self.ircbot = ircbot

    def setJabber(self, jabberbot):
        self.jabberbot = jabberbot

    def sendIRC(self, msg):
        if self.ircbot is not None:
            reactor.callLater(1, self.ircbot.sendMessage, msg)

    def sendJabber(self, msg):
        if self.jabberbot is not None:
            reactor.callLater(1, self.jabberbot.sendMessage, msg)

application = service.Application("ircjabberrelay")

manager = RelayManager()

# Configure IRC
ircfactory = IrcBotFactory(manager, '#channel', 'bot', manager.sendJabber)
#    point = TCP4ClientEndpoint(reactor, 'irc.freenode.net', 6667)
#    d = point.connect(ircfactory)
#    d.addCallback(gotProtocol)
connector = internet.TCPClient('irc.freenode.net', 6667, ircfactory)
connector.setServiceParent(application)

# Configure Jabber
xmppclient = XMPPClient(jid.internJID("jid@jabber.ru/bot"), "xxxxxxxx")
jabberbot = JabberBot(manager, "conference.jabber.ru", "channel", "bot", manager.sendIRC)
xmppclient.logTraffic = True
jabberbot.setHandlerParent(xmppclient)
xmppclient.setServiceParent(application)
manager.setJabber(jabberbot)
