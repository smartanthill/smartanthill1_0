# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

# pylint: disable=W0212,W0613

from twisted.python.failure import Failure
from twisted.trial.unittest import TestCase

import smartanthill.litemq.exchange as ex
from smartanthill.exception import LiteMQResendFailed


class LiteMQCase(TestCase):

    g_resent_nums = 0

    def test_declare_exchange(self):
        for type_, class_ in {"direct": ex.ExchangeDirect,
                              "fanout": ex.ExchangeFanout}.items():
            self.assertIsInstance(
                ex.ExchangeFactory().newExchange("exchange_name", type_),
                class_
            )

        self.assertRaises(
            AttributeError,
            lambda: ex.ExchangeFactory().newExchange("exchange_name",
                                                     "unknown-type")
        )

    def test_exchange_direct_ack_success(self):
        message, properties = "Test message", {"foo": "bar"}

        def _callback(m, p):
            self.assertEqual(m, message)
            self.assertEqual(p, properties)
            return True

        myex = ex.ExchangeFactory().newExchange("exchange_name", "direct")
        myex.bind_queue("queue_name", "routing_key", _callback, ack=True)

        empty_result = myex.publish("invalid_routing_key", message, properties)
        self.assertEqual(empty_result, [])

        result = myex.publish("routing_key", message, properties)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        d = result[0]

        def _resback(result):
            self.assertIsInstance(result, bool)
            self.assertEqual(result, True)
            myex.unbind_queue("queue_name")
            self.assertEqual(len(myex._queues), 0)

        d.addCallbacks(_resback)
        return d

    def test_exchange_direct_ack_problem(self):
        self.g_resent_nums, resend_max = 0, 3

        def _callback(m, p):
            self.g_resent_nums += 1
            # test exception
            if self.g_resent_nums == 1:
                return 1/0
            # test "ack-invalid" that is equl to False
            else:
                return False

        def _errback(result):
            self.assertIsInstance(result, Failure)
            self.assertTrue(result.check(LiteMQResendFailed))
            self.assertEqual(resend_max, self.g_resent_nums)

        myex = ex.ExchangeFactory().newExchange("exchange_name", "direct")
        myex.bind_queue("queue_name", "routing_key", _callback, ack=True)
        myex._queues['queue_name']._resend_max = resend_max
        myex._queues['queue_name']._resend_delay = 0
        result = myex.publish("routing_key", "Test message", {"foo": "bar"})

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        d = result[0]

        d.addBoth(_errback)
        return d

    def test_exchange_direct_nonack(self):
        self.g_resent_nums, resend_max = 0, 3

        def _callback(m, p):
            self.g_resent_nums += 1
            return 1/0

        def _errback(result):
            self.assertNotIsInstance(result, Failure)
            self.assertIsInstance(result, bool)
            self.assertEqual(result, False)

        myex = ex.ExchangeFactory().newExchange("exchange_name", "direct")
        myex.bind_queue("queue_name", "routing_key", _callback, ack=False)
        myex._queues['queue_name']._resend_max = resend_max
        myex._queues['queue_name']._resend_delay = 0
        result = myex.publish("routing_key", "Test message", {"foo": "bar"})

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        d = result[0]

        d.addBoth(_errback)
        return d
