# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from time import time

from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.python.constants import ValueConstant, Values

import smartanthill.network.cdc as cdc
from smartanthill.device.arg import DeviceIDArg
from smartanthill.network.zvd import ZeroVirtualDevice


class OperationType(Values):

    PING = ValueConstant(
        cdc.CHANNEL_URGENT.PING.value)
    LIST_OPERATIONS = ValueConstant(
        cdc.CHANNEL_BDCREQUEST.LIST_OPERATIONS.value)
    CONFIGURE_PIN_MODE = ValueConstant(
        cdc.CHANNEL_BDCREQUEST.CONFIGURE_PIN_MODE.value)
    READ_DIGITAL_PIN = ValueConstant(
        cdc.CHANNEL_BDCREQUEST.READ_DIGITAL_PIN.value)
    WRITE_DIGITAL_PIN = ValueConstant(
        cdc.CHANNEL_BDCREQUEST.WRITE_DIGITAL_PIN.value)
    CONFIGURE_ANALOG_REFERENCE = ValueConstant(
        cdc.CHANNEL_BDCREQUEST.CONFIGURE_ANALOG_REFERENCE.value)
    READ_ANALOG_PIN = ValueConstant(
        cdc.CHANNEL_BDCREQUEST.READ_ANALOG_PIN.value)
    WRITE_ANALOG_PIN = ValueConstant(
        cdc.CHANNEL_BDCREQUEST.WRITE_ANALOG_PIN.value)


class OperationBase(object):

    TYPE = None
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
        result = yield zvd.request(self.TYPE.value, self._devid, self.TTL,
                                   self.ACK, self.get_data())
        returnValue(self.on_result(result))


class EmptyArgsBase(OperationBase):

    def __init__(self, devidarg):
        OperationBase.__init__(self, devidarg)


class FiniteArgsBase(OperationBase):

    def __init__(self, devidarg, *args):
        OperationBase.__init__(self, devidarg)
        self._args = args

    def get_data(self):
        return [arg.get_value() for arg in self._args]


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

    TYPE = OperationType.PING

    def __init__(self, *args, **kwargs):
        EmptyArgsBase.__init__(self, *args, **kwargs)
        self._start = time()

    def on_result(self, result):
        return time() - self._start


class ListOperations(EmptyArgsBase):

    TYPE = OperationType.LIST_OPERATIONS


class ConfigurePinMode(InfinitePairArgsBase):

    TYPE = OperationType.CONFIGURE_PIN_MODE


class ReadDigitalPin(InfiniteSingleArgsBase):

    TYPE = OperationType.READ_DIGITAL_PIN


class WriteDigitalPin(InfinitePairArgsBase):

    TYPE = OperationType. WRITE_DIGITAL_PIN


class ConfigureAnalogReference(FiniteArgsBase):

    TYPE = OperationType.CONFIGURE_ANALOG_REFERENCE

    def __init__(self, devidarg, arefarg):
        FiniteArgsBase.__init__(self, devidarg, arefarg)


class ReadAnalogPin(InfiniteSingleArgsBase):

    TYPE = OperationType.READ_ANALOG_PIN

    def on_result(self, result):
        assert len(result) % 2 == 0
        newres = []
        while result:
            msb, lsb = result[0:2]
            del result[0:2]
            newres.append(msb << 8 | lsb)
        return newres


class WriteAnalogPin(InfinitePairArgsBase):

    TYPE = OperationType.WRITE_ANALOG_PIN
