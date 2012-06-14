import sys
from twisted.application import internet, service
from twisted.internet import reactor
from twisted.python import log
from twisted.words.protocols.jabber import jid
from wokkel.client import XMPPClient

import json

from ircbot import *
from jabberbot import *
from config import *

class RelayManager:
    def __init__(self):
        self.ircbot = None
        self.jabberbot = None
        self.ignoreList = []
        self.readIgnoreList()

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

    def addIgnore(self, nick):
        if nick in self.ignoreList:
            return
        self.ignoreList.append(nick)
        self.ignoreList.sort()
        self.writeIgnoreList()

    def removeIgnore(self, nick):
        if not nick in self.ignoreList:
            return
        self.ignoreList.remove(nick)
        self.writeIgnoreList()

    def readIgnoreList(self):
        try:
            f = open(IGNORE_LIST_FILEPATH, 'r')
            self.ignoreList = json.load(f)
            f.close()
        except:
            return

    def writeIgnoreList(self):
        s = json.dumps(self.ignoreList)
        f = open(IGNORE_LIST_FILEPATH, 'w')
        f.write(s)
        f.close()

def initIrcJabberRelay(application):
    manager = RelayManager()

    # Configure IRC
    ircfactory = IrcBotFactory(manager, cfg['ircchannel'], cfg['ircnick'], manager.sendJabber)
    # point = TCP4ClientEndpoint(reactor, 'irc.freenode.net', 6667)
    # d = point.connect(ircfactory)
    # d.addCallback(gotProtocol)
    connector = internet.TCPClient(cfg['ircserver'], cfg['ircport'], ircfactory)
    connector.setServiceParent(application)

    # Configure Jabber
    xmppclient = XMPPClient(jid.internJID(cfg['jabberjid']), cfg['jabberpass'])
    jabberbot = JabberBot(manager, cfg['jabberserver'], cfg['jabberchannel'], cfg['jabbernick'], manager.sendIRC)
    xmppclient.logTraffic = False
    jabberbot.setHandlerParent(xmppclient)
    xmppclient.setServiceParent(application)
    manager.setJabber(jabberbot)

