import sys
from twisted.internet import defer
from twisted.python import log
from twisted.words.protocols.jabber import jid
from wokkel import muc

class JabberBot(muc.MUCClient):
    """ """

    def __init__(self, manager, server, room, nick, callback):
        muc.MUCClient.__init__(self)
        self.manaer   = manager
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
            if body.startswith('/me '):
                self.callback("JABBER: * %s %s" % (user.nick, body.replace('/me ', '', 1)))
            else:
                self.callback("JABBER: <%s> %s" % (user.nick, body))

    def sendMessage(self, msg):
        #log.msg("jabber <- %s" % (msg))
        self.groupChat(self.room_jid, msg.decode('utf-8'))
