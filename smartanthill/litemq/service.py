# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from binascii import hexlify

from smartanthill.litemq.exchange import ExchangeFactory
from smartanthill.service import SAMultiService


class LiteMQService(SAMultiService):

    def __init__(self, name, options):
        SAMultiService.__init__(self, name, options)
        self._exchanges = {}

    def declare_exchange(self, name, type_="direct"):
        if name in self._exchanges:
            return

        self._exchanges[name] = ExchangeFactory().newExchange(name, type_)
        self.log.debug("Declared new exchange '%s' with type '%s'" % (
            name, type_))

    def undeclare_exchange(self, name):
        if not name in self._exchanges:
            return

        del self._exchanges[name]
        self.log.debug("Undeclared exchange '%s'" % name)

    def produce(self, exchange, routing_key, message, properties=None):
        assert exchange in self._exchanges
        self._exchanges[exchange].publish(routing_key, message, properties)
        self.log.debug(
          "Produced new message '%s' with routing_key '%s' " "to exchange '%s'"
          % (hexlify(message) if properties and "binary" in properties and
             properties["binary"] else message, routing_key, exchange))
    def consume(self, exchange, queue, routing_key, callback, ack=False):
        assert exchange in self._exchanges
        self._exchanges[exchange].bind_queue(queue, routing_key, callback, ack)
        self.log.debug("Registered consumer with exchange=%s, queue=%s, "
                       "routing_key=%s, ack=%s" % (
                           exchange, queue, routing_key, ack))

    def unconsume(self, exchange, queue):
        assert exchange in self._exchanges
        self._exchanges[exchange].unbind_queue(queue)
        self.log.debug("Unregistered consumer with exchange=%s "
                       "and queue=%s" % (exchange, queue))


def makeService(name, options):
    return LiteMQService(name, options)
