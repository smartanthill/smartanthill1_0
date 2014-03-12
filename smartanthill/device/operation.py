# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from twisted.internet.defer import Deferred, inlineCallbacks,  returnValue

import smartanthill.network.cdc as cdc
from smartanthill.network.zvd import ZeroVirtualDevice


class OperationBase(object):

    CDC =  None
    TTL = 1
    ACK = True

    def __init__(self):
        self._devid = 0

    def get_devid(self):
        return self.devid

    def get_data(self):
        return None

    def on_result(self, result):
        return result

    @inlineCallbacks
    def launch(self):
        zvd = ZeroVirtualDevice()
        result = yield zvd.request(self.CDC, self.get_devid(), self.TTL, self.ACK,
                             self.get_data())
        returnValue(self.on_result(result))


class EmptyArgsBase(OperationBase):

    def __init__(self, devidarg):
        self.devid = devidarg.get_value()


class InfiniteArgsBase(OperationBase):

    def __init__(self, *args):
        self._args = args

    def get_data(self):
        return [arg.get_value() for arg in self._args]


class InfiniteSingleArgsBase(InfiniteArgsBase):

    def __init__(self, *args):
        assert len(args) >= 2
        self.devid = args[0].get_value()
        self._args = args[1:]


class InfinitePairArgsBase(InfiniteArgsBase):

    def __init__(self, *args):
        assert len(args) >= 3 and len(args) % 2 != 0
        self.devid = args[0].get_value()
        self._args = args[1:]


class Ping(EmptyArgsBase):

    CDC = cdc.CHANNEL_URGENT.PING


class ListOperationalStates(EmptyArgsBase):

    CDC = cdc.CHANNEL_BDCREQUEST.LIST_OPERATIONAL_STATES


class ConfigurePinMode(InfinitePairArgsBase):

    CDC = cdc.CHANNEL_BDCREQUEST.CONFIGURE_PIN_MODE


class ReadDigitalPin(InfiniteSingleArgsBase):

    CDC = cdc.CHANNEL_BDCREQUEST.READ_DIGITAL_PIN


class WriteDigitalPin(InfinitePairArgsBase):

    CDC = cdc.CHANNEL_BDCREQUEST.WRITE_DIGITAL_PIN


class ConfigureAnalogReference(InfiniteSingleArgsBase):

    CDC = cdc.CHANNEL_BDCREQUEST.CONFIGURE_ANALOG_REFERENCE

    def __init__(self, devidarg, arefarg):
        self.devid = devidarg.get_value()
        self._aref = arefarg.get_value()

    def get_data(self):
        return [self._aref]


class ReadAnalogPin(InfiniteSingleArgsBase):

    CDC = cdc.CHANNEL_BDCREQUEST.READ_ANALOG_PIN

    def on_result(self, result):
        assert len(result) % 2 == 0
        newres = []
        while result:
            msb, lsb = result[0:2]
            del result[0:2]
            newres.append(msb << 8 | lsb)
        return newres
