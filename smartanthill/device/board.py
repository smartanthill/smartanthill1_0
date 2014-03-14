# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from inspect import isfunction

from twisted.python.reflect import namedAny

import smartanthill.device.arg as arg
import smartanthill.device.operation as op
from smartanthill.exception import (OperArgNumsExceeded, UnknownBoardOperation,
                                    UnknownDeviceBoard)


class BoardFactory(object):

    @staticmethod
    def newBoard(name):
        obj_path = "smartanthill.device.board.Board%s" % name.title()
        try:
            obj = namedAny(obj_path)()
        except AttributeError:
            raise UnknownDeviceBoard(name)
        assert isinstance(obj, BoardBase)
        return obj


class BoardBase(object):

    PINS_ALIAS = None
    PINS = None
    ANALOG_PINS = None


    OPERATION_SETTINGS = {
        "ping": (
            op.Ping,
        ),

        "listoperationalstates": (
            op.ListOperationalStates,
        ),

        "configurepinmode": (
            op.ConfigurePinMode,
            (arg.PinArg, [lambda s: s.PINS, lambda s: s.PINS_ALIAS]),
            [arg.PinModeArg, None],
            "infinite"
        ),

        "readdigitalpin": (
            op.ReadDigitalPin,
            (arg.PinArg, [lambda s: s.PINS, lambda s: s.PINS_ALIAS]),
            "infinite"
        ),

        "writedigitalpin": (
            op.WriteDigitalPin,
            (arg.PinArg, [lambda s: s.PINS, lambda s: s.PINS_ALIAS]),
            (arg.PinLevelArg, ()),
            "infinite"
        ),

        "configureanalogreference": (
            op.ConfigureAnalogReference,
            [arg.PinAnalogRefArg, None]
        ),

        "readanalogpin": (
            op.ReadAnalogPin,
            (arg.PinArg, [lambda s: s.ANALOG_PINS, lambda s: s.PINS_ALIAS]),
            "infinite"
        )
    }

    def launch_device_operation(self, devid, name, *args):
        try:
            operset = self.OPERATION_SETTINGS[name.lower()]
        except:
            raise UnknownBoardOperation(name, self.__class__.__name__)

        if operset[-1] != "infinite" and len(args) != len(operset)-1:
            raise OperArgNumsExceeded(len(args), len(operset)-1, name)

        # process lambdas for args
        for _index, _item in enumerate(operset):
            if type(_item) != tuple or len(_item) != 2:
                continue
            for _argindex, _argarg in enumerate(_item[1]):
                if isfunction(_argarg):
                    operset[_index][1][_argindex] = _argarg(self)

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

            if _index+1 < len(operset) and operset[_index+1] == "infinite":
                _index = 1
            else:
                _index += 1

        return operset[0](*classargs).launch()


class BoardArduino(BoardBase):

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

    def __init__(self):
        # define allowed modes
        self.OPERATION_SETTINGS['configurepinmode'][2][1] = (
            (0, 1, 2),
            dict(INPUT=0, OUTPUT=1, INPUT_PULLUP=2)
        )
        # define allowed analog references
        self.OPERATION_SETTINGS['configureanalogreference'][1][1] = (
            range(0, 3),
            dict(DEFAULT=0, EXTERNAL=1, INTERNAL=2)
        )


class BoardArduino_Pro5V(BoardArduino):

    PINS = range(1, 22)
    ANALOG_PINS = range(14, 22)
