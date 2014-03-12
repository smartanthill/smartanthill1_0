# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from binascii import hexlify

from twisted.application.service import MultiService, Service
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, maybeDeferred, returnValue
from twisted.internet.serialport import SerialPort

import smartanthill.network.protocol as p
from smartanthill.exception import NetworkRouterConnectFailure
from smartanthill.log import Logger


class ControlService(Service):

    def __init__(self, sas):
        self.setName("network.control")
        self.log = Logger(self)
        self.sas = sas
        self.protocol = p.ControlProtocolWrapping(self.climessage_protocallback)

    def startService(self):
        self.protocol.makeConnection(self)

        self.sas.litemq.consume("network", "control.in",
                                "transport->control",
                                self.inmessage_mqcallback)
        self.sas.litemq.consume("network", "control.out",
                                "client->control",
                                self.outmessage_mqcallback)

        Service.startService(self)
        self.log.info("Service has been started.")

    def stopService(self):
        Service.stopService(self)
        self.log.info("Service has been stopped.")

    def write(self, message):
        self.sas.litemq.produce("network", "control->transport", message,
                                dict(binary=True))

    def inmessage_mqcallback(self, message, properties):
        self.log.debug("Received incoming raw message %s" % hexlify(message))
        self.protocol.dataReceived(message)

    def outmessage_mqcallback(self, message, properties):
        self.log.debug("Received outgoing %s and properties=%s" %
                       (message, properties))
        self.protocol.send_message(message)

    def climessage_protocallback(self, message):
        self.log.debug("Received incoming client %s" % message)
        self.sas.litemq.produce("network", "control->client", message)


class TransportService(Service):

    def __init__(self, sas):
        self.setName("network.transport")
        self.log = Logger(self)
        self.sas = sas
        self.protocol = p.TransportProtocolWrapping(
            self.inmessage_protocallback)

    def startService(self):
        self.protocol.makeConnection(self)

        self.sas.litemq.consume("network", "transport.in",
                                "routing->transport",
                                self.insegment_mqcallback)
        self.sas.litemq.consume("network", "transport.out",
                                "control->transport",
                                self.outmessage_mqcallback, ack=True)

        Service.startService(self)
        self.log.info("Service has been started.")

    def stopService(self):
        Service.stopService(self)
        self.sas.litemq.unconsume("network", "transport.in")
        self.sas.litemq.unconsume("network", "transport.out")
        self.log.info("Service has been stopped.")

    def inmessage_protocallback(self, message):
        self.log.debug("Received incoming message %s" % hexlify(message))
        self.sas.litemq.produce("network", "transport->control", message,
                                dict(binary=True))

    def write(self, segment):
        self.sas.litemq.produce("network", "transport->routing", segment,
                                dict(binary=True))

    def insegment_mqcallback(self, message, properties):
        self.log.debug("Received incoming segment %s" % hexlify(message))
        self.protocol.dataReceived(message)

    @inlineCallbacks
    def outmessage_mqcallback(self, message, properties):
        self.log.debug("Received outgoing message %s" % hexlify(message))
        ctrlmsg = p.ControlProtocol.rawmessage_to_message(message)
        d = maybeDeferred(self.protocol.send_message, message)
        result = yield d
        if result and ctrlmsg.ack:
            self.sas.litemq.produce("network", "acknowledged->client", ctrlmsg)
        returnValue(result)


class RouterService(Service):

    INSTANCE_ORDER = 0
    RECONNECT_DELAY = 1  # in seconds

    def __init__(self, sas, options):
        RouterService.INSTANCE_ORDER += 1
        self.setName("network.router.%d" % RouterService.INSTANCE_ORDER)
        self.log = Logger(self)
        self.sas = sas
        self.options = options
        self.protocol = p.RoutingProtocolWrapping(self.inpacket_protocallback)
        self._reconnect_nums = 0

    def startService(self):
        try:
            if self.options['type'] == "serial":
                SerialPort(self.protocol, self.options['port'], reactor,
                           baudrate=int(self.options['baudrate']))
        except Exception, e:
            self.log.error(NetworkRouterConnectFailure(self.options))
            self._reconnect_nums += 1
            reactor.callLater(self._reconnect_nums * self.RECONNECT_DELAY,
                              self.startService)
            return

        self.sas.litemq.consume("network", "routing.out",
                                "transport->routing",
                                self.outsegment_mqcallback)

        Service.startService(self)
        self.log.info("Service has been started with options '%s'" %
                      self.options)

    def stopService(self):
        Service.stopService(self)
        self.sas.litemq.unconsume("network", "routing.out")
        self.log.info("Service has been stopped.")

    def inpacket_protocallback(self, packet):
        self.log.debug("Received incoming packet %s" % hexlify(packet))
        self.sas.litemq.produce("network", "routing->transport",
                                p.RoutingProtocol.packet_to_segment(packet),
                                dict(binary=True))

    def outsegment_mqcallback(self, message, properties):
        # check destination ID
        if not ord(message[2]) in self.options['deviceids']:
            return False
        self.log.debug("Received outgoing segment %s" % hexlify(message))
        self.protocol.send_segment(message)


class NetworkService(MultiService):

    def __init__(self, sas, options):
        MultiService.__init__(self)
        self.setName("network")
        self.log = Logger(self)
        self.sas = sas
        self.options = options

    def startService(self):
        self.sas.litemq.declare_exchange("network")

        self.addService(ControlService(self.sas))
        self.addService(TransportService(self.sas))

        for opt in self.options['routers']:
            self.addService(RouterService(self.sas, opt))

        MultiService.startService(self)
        self.log.info("Service has been started with options '%s'" %
                      self.options)

    def stopService(self):
        MultiService.stopService(self)
        self.sas.litemq.undeclare_exchange("network")
        self.log.info("Service has been stopped.")


def makeService(sas, options):
    return NetworkService(sas, options)
