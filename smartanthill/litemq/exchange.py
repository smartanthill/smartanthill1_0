# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.python.failure import Failure
from twisted.python.reflect import namedAny

from smartanthill.exception import (LiteMQACKFailed, LiteMQResendFailed,
                                    NotImplemnetedYet)
from smartanthill.log import Logger
from smartanthill.service import SmartAnthillService


class ExchangeFactory(object):

    @staticmethod
    def newExchange(name, type_):
        obj_path = "smartanthill.litemq.exchange.Exchange%s" % type_.title()
        obj = namedAny(obj_path)(name)
        assert isinstance(obj, ExchangeBase)
        return obj


class Queue(object):

    def __init__(self, name, routing_key):
        self.log = Logger("litemq.queue")
        self.name = name
        self.routing_key = routing_key

        _litemq = SmartAnthillService.instance().getServiceNamed("litemq")
        self._resend_delay = _litemq.options['resend_delay']
        self._resend_max = _litemq.options['resend_max']
        self._callbacks = []

    def attach_callback(self, callback, ack=False):
        assert callable(callback)
        self._callbacks.append((callback, ack))

    def put(self, message, properties):
        assert self._callbacks
        d = Deferred()
        for c in self._callbacks:
            d.addCallback(lambda r, c, m, p: c(m, p), c[0], message, properties)
            if c[1]:
                d.addCallback(lambda r: True if isinstance(r, bool) and r else
                              Failure(LiteMQACKFailed()))
        d.addErrback(self._d_errback_callback, message, properties)
        reactor.callWhenRunning(d.callback, True)

    def _d_errback_callback(self, failure, message, properties):
        self.log.warn(failure, message, properties)
        if "_resentnums" not in properties:
            properties["_resentnums"] = 0
        properties["_resentnums"] += 1

        if properties["_resentnums"] > self._resend_max:
            raise LiteMQResendFailed

        reactor.callLater(self._resend_delay * properties["_resentnums"],
                          self.put, message, properties)


class ExchangeBase(object):

    def __init__(self, name):
        self.name = name
        self._queues = {}

    def bind_queue(self, name, routing_key, callback, ack):
        if name not in self._queues:
            self._queues[name] = Queue(name, routing_key)
        self._queues[name].attach_callback(callback, ack)

    def unbind_queue(self, name):
        if name in self._queues:
            del self._queues[name]

    def publish(self, routing_key, message, properties):
        pass


class ExchangeDirect(ExchangeBase):

    def publish(self, routing_key, message, properties):
        for q in self._queues.itervalues():
            if q.routing_key == routing_key:
                q.put(message, properties)


class ExchangeFanout(ExchangeBase):

    def publish(self, routing_key, message, properties):
        for q in self._queues.itervalues():
            q.put(message, properties)


class ExchangeTopic(ExchangeBase):

    def publish(self, routing_key, message, properties):
        raise NotImplemnetedYet
        for q in self._queues.itervalues():
            if self.match(routing_key, q.routing_key):
                q.put(message, properties)

    def match(self, routing_key, routing_pattern):
        # TODO
        raise NotImplementedError
