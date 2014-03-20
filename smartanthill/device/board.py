# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from inspect import isfunction

from twisted.python.reflect import namedAny

import smartanthill.device.arg as arg
import smartanthill.device.operation as op
from smartanthill.exception import (BoardUnknownOperation, DeviceUnknownBoard,
                                    OperArgNumsExceeded, OperArgNumsNeed,
                                    OperArgNumsPairedNeed)


class BoardFactory(object):

    @staticmethod
    def newBoard(name):
        obj_path = "smartanthill.device.board.Board%s" % name.title()
        try:
            obj = namedAny(obj_path)()
        except AttributeError:
            raise DeviceUnknownBoard(name)
        assert isinstance(obj, BoardBase)
        return obj


class BoardBase(object):

    PINS_ALIAS = None
    PINS = None
    ANALOG_PINS = None


    OPERATION_SETTINGS = [
        (
            op.Ping,
        ),
        (
            op.ListOperations,
        ),
        (
            op.ConfigurePinMode,
            (arg.PinArg, [lambda s: s.PINS, lambda s: s.PINS_ALIAS]),
            [arg.PinModeArg, lambda s: s.get_pinmodeargset()]
        ),
        (
            op.ReadDigitalPin,
            (arg.PinArg, [lambda s: s.PINS, lambda s: s.PINS_ALIAS])
        ),
        (
            op.WriteDigitalPin,
            (arg.PinArg, [lambda s: s.PINS, lambda s: s.PINS_ALIAS]),
            (arg.PinLevelArg, ())
        ),
        (
            op.ConfigureAnalogReference,
            [arg.PinAnalogRefArg, lambda s: s.get_pinanalogrefargset()]
        ),
        (
            op.ReadAnalogPin,
            (arg.PinArg, [lambda s: s.ANALOG_PINS, lambda s: s.PINS_ALIAS])
        ),
    ]

    def get_operset(self, type_):
        for operset in self.OPERATION_SETTINGS:
            if operset[0].TYPE == type_:
                return operset
        raise BoardUnknownOperation(type_.name, self.__class__.__name__)

    def get_pinmodeargset(self):
        raise NotImplementedError()

    def get_pinanalogrefargset(self):
        raise NotImplementedError()

    def launch_device_operation(self, devid, type_, *args):
        operset = self.get_operset(type_)
        self._operset_validate_cliargs(operset, args)
        operset = self._operset_process_lambdas(operset)

        # the first argument for operation should be DeviceIDArg
        classargs = [arg.DeviceIDArg()]
        classargs[0].set_value(devid)

        # populate client's arguments
        _index = 1
        for _argvalue in args:
            _argset = operset[_index]
            _argobj = _argset[0](*_argset[1])
            _argobj.set_value(_argvalue)
            classargs.append(_argobj)

            if (_index+1 == len(operset) and
                    issubclass(operset[0], op.InfiniteArgsBase)):
                _index = 1
            else:
                _index += 1
        return operset[0](*classargs).launch()

    def _operset_validate_cliargs(self, operset, args):
        type_name = operset[0].TYPE.name
        if issubclass(operset[0], op.InfiniteArgsBase):
            if len(args) < len(operset)-1:
                raise OperArgNumsNeed(len(operset)-1, type_name, len(args))
            elif (issubclass(operset[0], op.InfinitePairArgsBase)
                  and len(args) % 2 != 0):
                raise OperArgNumsPairedNeed(type_name, len(args))
        elif len(args) != len(operset)-1:
            raise OperArgNumsExceeded(len(args), type_name, len(operset)-1)

    def _operset_process_lambdas(self, operset):
        for _index, _item in enumerate(operset):
            if _index == 0 or len(_item) != 2:
                continue
            elif isfunction(_item[1]):
                operset[_index][1] = _item[1](self)
            else:
                for _argindex, _argarg in enumerate(_item[1]):
                    if isfunction(_argarg):
                        operset[_index][1][_argindex] = _argarg(self)
        return operset

class BoardArduino(BoardBase):

    PINS = range(1, 22)
    PINS_ALIAS = dict(
        SS=10,
        MOSI=11,
        MISO=12,
        SCK=13,

        SDA=18,
        SCL=19,
        LED_BUILTIN=13,

        A0=14,
        A1=15,
        A2=16,
        A3=17,
        A4=18,
        A5=19,
        A6=20,
        A7=21
    )
    ANALOG_PINS = range(14, 22)

    def get_pinmodeargset(self):
        return ((0, 1, 2), dict(INPUT=0, OUTPUT=1, INPUT_PULLUP=2))

    def get_pinanalogrefargset(self):
        return (range(0, 3), dict(DEFAULT=0, EXTERNAL=1, INTERNAL=2))


class BoardArduino_Pro5V(BoardArduino):

    INFO_URL = "http://arduino.cc/en/Main/ArduinoBoardProMini"

