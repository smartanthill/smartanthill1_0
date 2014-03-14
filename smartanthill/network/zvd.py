# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from twisted.internet.defer import Deferred

from smartanthill.network.protocol import ControlMessage
from smartanthill.service import SmartAnthillService
from smartanthill.util import singleton


@singleton
class ZeroVirtualDevice(object):

    ID = 0x0

    def __init__(self):
        self._litemq = SmartAnthillService.instance().getServiceNamed("litemq")
        self._litemq.consume("network", "msgqueue", "control->client",
                             self.onmessage_mqcallback)
        self._litemq.consume("network", "ackqueue", "acknowledged->client",
                             self.onack_mqcallback)
        self._resqueue = []
        self._ackqueue = []

    def request(self, cdc, destination, ttl, ack, data):
        cm = ControlMessage(cdc, self.ID, destination, ttl, ack, data)
        self._litemq.produce("network", "client->control", cm)
        return self._defer_result(cm)

    def _defer_result(self, message):
        d = Deferred()
        if message.is_bdcrequest():
            self._resqueue.append((d, message))
        else:
            self._ackqueue.append((d, message))
        return d

    def onmessage_mqcallback(self, message, properties):
        if not message.is_bdcresponse():
            return

        for item in self._resqueue:
            if (item[1].get_dataclassifier() == message.get_dataclassifier()
                    and item[1].source == message.destination
                    and item[1].destination == message.source):
                item[0].callback(message.data)
                self._resqueue.remove(item)
                return True

    def onack_mqcallback(self, message, properties):
        for item in self._ackqueue:
            if item[1] == message:
                item[0].callback(True)
                self._ackqueue.remove(item)
                return True
