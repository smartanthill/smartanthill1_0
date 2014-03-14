# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from binascii import hexlify

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, maybeDeferred, returnValue
from twisted.internet.serialport import SerialPort

import smartanthill.network.protocol as p
from smartanthill.exception import NetworkRouterConnectFailure
from smartanthill.service import SAMultiService


class ControlService(SAMultiService):

    def __init__(self, name):
        SAMultiService.__init__(self, name)
        self._protocol = p.ControlProtocolWrapping(
          self.climessage_protocallback)
        self._litemq = None

    def startService(self):
        self._litemq = self.parent.parent.getServiceNamed("litemq")
        self._protocol.makeConnection(self)
        self._litemq.consume("network", "control.in", "transport->control",
                             self.inmessage_mqcallback)
        self._litemq.consume("network", "control.out", "client->control",
                             self.outmessage_mqcallback)
        SAMultiService.startService(self)

    def stopService(self):
        SAMultiService.stopService(self)
        self._litemq.unconsume("network", "control.in")
        self._litemq.unconsume("network", "control.out")

    def write(self, message):
        self._litemq.produce("network", "control->transport", message,
                             dict(binary=True))

    def inmessage_mqcallback(self, message, properties):
        self.log.debug("Received incoming raw message %s" % hexlify(message))
        self._protocol.dataReceived(message)

    def outmessage_mqcallback(self, message, properties):
        self.log.debug("Received outgoing %s and properties=%s" %
                       (message, properties))
        self._protocol.send_message(message)

    def climessage_protocallback(self, message):
        self.log.debug("Received incoming client %s" % message)
        self._litemq.produce("network", "control->client", message)


class TransportService(SAMultiService):

    def __init__(self, name):
        SAMultiService.__init__(self, name)
        self._protocol = p.TransportProtocolWrapping(
            self.inmessage_protocallback)
        self._litemq = None

    def startService(self):
        self._litemq = self.parent.parent.getServiceNamed("litemq")
        self._protocol.makeConnection(self)
        self._litemq.consume("network", "transport.in", "routing->transport",
                             self.insegment_mqcallback)
        self._litemq.consume("network", "transport.out", "control->transport",
                             self.outmessage_mqcallback, ack=True)
        SAMultiService.startService(self)

    def stopService(self):
        SAMultiService.stopService(self)
        self._litemq.unconsume("network", "transport.in")
        self._litemq.unconsume("network", "transport.out")

    def inmessage_protocallback(self, message):
        self.log.debug("Received incoming message %s" % hexlify(message))
        self._litemq.produce("network", "transport->control", message,
                             dict(binary=True))

    def write(self, segment):
        self._litemq.produce("network", "transport->routing", segment,
                             dict(binary=True))

    def insegment_mqcallback(self, message, properties):
        self.log.debug("Received incoming segment %s" % hexlify(message))
        self._protocol.dataReceived(message)

    @inlineCallbacks
    def outmessage_mqcallback(self, message, properties):
        self.log.debug("Received outgoing message %s" % hexlify(message))
        ctrlmsg = p.ControlProtocol.rawmessage_to_message(message)
        d = maybeDeferred(self._protocol.send_message, message)
        result = yield d
        if result and ctrlmsg.ack:
            self._litemq.produce("network", "acknowledged->client", ctrlmsg)
        returnValue(result)


class RouterService(SAMultiService):

    RECONNECT_DELAY = 1  # in seconds

    def __init__(self, name, options):
        SAMultiService.__init__(self, name, options)
        self._protocol = p.RoutingProtocolWrapping(self.inpacket_protocallback)
        self._litemq = None
        self._reconnect_nums = 0

    def startService(self):
        try:
            if self.options['type'] == "serial":
                SerialPort(self._protocol, self.options['port'], reactor,
                           baudrate=int(self.options['baudrate']))
        except:
            self.log.error(NetworkRouterConnectFailure(self.options))
            self._reconnect_nums += 1
            reactor.callLater(self._reconnect_nums * self.RECONNECT_DELAY,
                              self.startService)
            return

        self._litemq = self.parent.parent.getServiceNamed("litemq")
        self._litemq.consume("network", "routing.out", "transport->routing",
                             self.outsegment_mqcallback)
        SAMultiService.startService(self)

    def stopService(self):
        SAMultiService.stopService(self)
        self._litemq.unconsume("network", "routing.out")

    def inpacket_protocallback(self, packet):
        self.log.debug("Received incoming packet %s" % hexlify(packet))
        self._litemq.produce("network", "routing->transport",
                             p.RoutingProtocol.packet_to_segment(packet),
                             dict(binary=True))

    def outsegment_mqcallback(self, message, properties):
        # check destination ID
        if not ord(message[2]) in self.options['deviceids']:
            return False
        self.log.debug("Received outgoing segment %s" % hexlify(message))
        self._protocol.send_segment(message)


class NetworkService(SAMultiService):

    def __init__(self, name, options):
        SAMultiService.__init__(self, name, options)
        self._litemq = None

    def startService(self):
        self._litemq = self.parent.getServiceNamed("litemq")
        self._litemq.declare_exchange("network")

        ControlService("network.control").setServiceParent(self)
        TransportService("network.transport").setServiceParent(self)

        num = 0
        for opt in self.options['routers']:
            num += 1
            RouterService("network.router.%d" % num, opt).setServiceParent(self)

        SAMultiService.startService(self)

    def stopService(self):
        SAMultiService.stopService(self)
        self._litemq.undeclare_exchange("network")


def makeService(name, options):
    return NetworkService(name, options)
