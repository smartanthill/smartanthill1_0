# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from twisted.internet.defer import inlineCallbacks, returnValue

import smartanthill.network.cdc as cdc
from smartanthill.network.zvd import ZeroVirtualDevice
from smartanthill.device.arg import DeviceIDArg


class OperationBase(object):

    CDC = None
    TTL = 1
    ACK = True

    def __init__(self, devidarg):
        assert isinstance(devidarg, DeviceIDArg)
        self._devid = devidarg.get_value()

    def get_data(self):
        return []

    def on_result(self, result):
        return result

    @inlineCallbacks
    def launch(self):
        zvd = ZeroVirtualDevice()
        result = yield zvd.request(self.CDC, self._devid, self.TTL,
                                   self.ACK, self.get_data())
        returnValue(self.on_result(result))


class EmptyArgsBase(OperationBase):

    def __init__(self, devidarg):
        OperationBase.__init__(self, devidarg)


class InfiniteArgsBase(OperationBase):

    def __init__(self, devidarg, *args):
        OperationBase.__init__(self, devidarg)
        self._args = args

    def get_data(self):
        return [arg.get_value() for arg in self._args]


class InfiniteSingleArgsBase(InfiniteArgsBase):

    def __init__(self, devidarg, *args):
        assert len(args) >= 1
        InfiniteArgsBase.__init__(self, devidarg, *args)


class InfinitePairArgsBase(InfiniteArgsBase):

    def __init__(self, devidarg, *args):
        assert len(args) >= 2 and len(args) % 2 == 0
        InfiniteArgsBase.__init__(self, devidarg, *args)


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
        InfiniteSingleArgsBase.__init__(self, devidarg, arefarg)


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
