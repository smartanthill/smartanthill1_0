# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

# pylint: disable=W0613

from twisted.internet.defer import Deferred

from smartanthill.exception import DeviceNotResponding
from smartanthill.network.protocol import ControlMessage
from smartanthill.util import get_service_named, singleton


@singleton
class ZeroVirtualDevice(object):

    ID = 0x0

    def __init__(self):
        self._litemq = get_service_named("litemq")
        self._litemq.consume("network", "msgqueue", "control->client",
                             self.onresult_mqcallback)
        self._litemq.consume("network", "ackqueue", "transport->ack",
                             self.onack_mqcallback)
        self._litemq.consume("network", "errqueue", "transport->err",
                             self.onerr_mqcallback)
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
            self._ackqueue.append([d, message, 0])
        return d

    def onresult_mqcallback(self, message, properties):
        if not message.is_bdcresponse():
            return

        for item in self._resqueue:
            conds = [
                item[1].get_dataclassifier() == message.get_dataclassifier(),
                item[1].source == message.destination,
                item[1].destination == message.source
            ]
            if all(conds):
                self._resqueue.remove(item)
                item[0].callback(message.data)
                return True

    def onack_mqcallback(self, message, properties):
        for item in self._ackqueue:
            if item[1] == message:
                self._ackqueue.remove(item)
                item[0].callback(True)
                break

    def onerr_mqcallback(self, message, properties):
        for item in self._ackqueue:
            if item[1] == message:
                if item[2] == self._litemq.options['resend_max']:
                    self._ackqueue.remove(item)
                    item[0].errback(DeviceNotResponding(message.destination,
                                                        item[2]))
                else:
                    item[2] += 1
                break
