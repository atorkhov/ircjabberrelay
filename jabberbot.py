# -*- coding: utf-8 -*-

import sys
from twisted.internet import defer
from twisted.python import log
from twisted.words.protocols.jabber import jid
from wokkel import muc

class JabberBot(muc.MUCClient):
    """ """

    def __init__(self, manager, server, room, nick, callback):
        muc.MUCClient.__init__(self)
        self.manager   = manager
        self.server   = server
        self.room     = room
        self.nick     = nick
        self.callback = callback
        self.room_jid = jid.internJID(self.room+'@'+self.server+'/'+self.nick)

    def initialized(self):
        """The bot has connected to the xmpp server, now try to join the room.
        """
        log.msg("Connected to server")
        self.join(self.server, self.room, self.nick).addCallback(self.initRoom)

    @defer.inlineCallbacks
    def initRoom(self, room):
        """Configure the room if we just created it.
        """

        if int(room.status) == muc.STATUS_CODE_CREATED:
            config_form = yield self.getConfigureForm(self.room_jid.userhost())

            # set config default
            config_result = yield self.configure(self.room_jid.userhost())

    def receivedGroupChat(self, room, user, body):
        if not user.nick.startswith(self.nick):
            #if body.startswith('/me '):
            #    self.callback("JABBER: * %s %s" % (user.nick, body.replace('/me ', '', 1)))
            #else:

            # send to irc only command messages
            if body.startswith('@toirc1251 '):
                msg = body.replace('@toirc1251 ', '', 1).rstrip()
                msg = "JABBER: <%s> %s" % (user.nick, msg)
                try:
                    msg = msg.encode('cp1251')
                except UnicodeDecodeError:
                    None
                self.callback(msg)
            elif body.startswith('@toirc '):
                msg = "JABBER: <%s> %s" % (user.nick, body.replace('@toirc ', '', 1))
                msg = msg.rstrip().encode('utf-8')
                self.callback(msg)
            elif body.startswith('@help'):
                self.sendMessage('\n'.join(
                    [u"@toirc <сообщение> - послать сообщение в IRC",
                     u"@toirc1251 <сообщение> - послать сообщение в IRC в кодировке CP1251",
                     u"@who - выводит список пользователей на IRC канале"
                    ]).encode('utf-8'))
            elif body.startswith('@who'):
                if self.manager.ircbot is not None:
                    self.manager.ircbot.names().addCallback(self.printOnline)

    def printOnline(self, namelist):
        namelist.sort()
        msg = ' '.join(namelist)
        self.groupChat(self.room_jid, msg.decode('utf-8'))

    def sendMessage(self, msg):
        #log.msg("jabber <- %s" % (msg))
        self.groupChat(self.room_jid, msg.decode('utf-8'))
