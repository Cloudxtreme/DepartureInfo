__author__ = 'Reuben'
from twisted.internet import reactor, endpoints, protocol, defer
import sys

class ServerProtocol(protocol.Protocol):
    def connectionMade(self):
        print 'Client connected'
        x = self.transport
        self.transport.write('Hello Client!')
        self.factory.connections.append(x)
    def connectionLost(self, reason):
        x = self.transport
        print 'Client Disconnected'
        self.factory.connections.remove(x)
    def dataReceived(self, data):
        print 'Received and sending', data
        for connection in self.factory.connections:
            if connection == self.transport:
                pass
            else:
                connection.write(data)


class IDSFactory(protocol.ServerFactory):
    protocol = ServerProtocol
    connections = []

endpoints.serverFromString(reactor, 'tcp:8000').listen(IDSFactory())
reactor.run()
