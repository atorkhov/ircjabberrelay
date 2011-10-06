from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

class IrcBot(irc.IRCClient):
    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def signedOn(self):
        self.join(self.factory.channel)
        log.msg("Signed on as %s." % (self.nickname,))
        self.factory.manager.setIRC(self)

    def joined(self, channel):
        log.msg("Joined %s." % (channel,))

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        user = user.split('!', 1)[0]

        # Check to see if they're sending me a private message
        if channel == self.nickname:
            return

        if self.isUtf8(msg):
            self.factory.callback("IRC: <%s> %s" % (user, msg.rstrip()))
        else:
            self.factory.callback("IRC (CP1251): <%s> %s" % (user, msg.decode('cp1251').encode('utf-8').rstrip()))

    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        user = user.split('!', 1)[0]

        if self.isUtf8(msg):
            self.factory.callback("IRC: * %s %s" % (user, msg.rstrip()))
        else:
            self.factory.callback("IRC (CP1251): * %s %s" % (user, msg.decode('cp1251').encode('utf-8').rstrip()))

    def sendMessage(self, msg):
        #log.msg("irc <- %s" % (msg))
        self.msg(self.factory.channel, msg)

    def isUtf8(self, msg):
        try:
            msg.decode('utf-8')
            return True
        except UnicodeDecodeError:
            return False

class IrcBotFactory(protocol.ClientFactory):
    protocol = IrcBot

    def __init__(self, manager, channel, nickname, callback):
        self.manager = manager
        self.channel = channel
        self.nickname = nickname
        self.callback = callback

    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)
        reactor.stop()
