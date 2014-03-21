# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from twisted.python.reflect import namedAny

from smartanthill.device.operation.base import get_operclass, OperationType
from smartanthill.exception import BoardUnknownOperation, DeviceUnknownBoard


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
    PWM_PINS = None
    OPERATIONS = [
        OperationType.PING,
        OperationType.LIST_OPERATIONS,
        OperationType.CONFIGURE_PIN_MODE,
        OperationType.READ_DIGITAL_PIN,
        OperationType.WRITE_DIGITAL_PIN,
        OperationType.READ_ANALOG_PIN,
        OperationType.WRITE_ANALOG_PIN,
        OperationType.CONFIGURE_ANALOG_REFERENCE
    ]

    def get_pinarg_params(self):
        return (self.PINS, self.PINS_ALIAS)

    def get_analogpinarg_params(self):
        return (self.ANALOG_PINS, self.PINS_ALIAS)

    def get_pwmpinarg_params(self):
        return (self.PWM_PINS, self.PINS_ALIAS)

    def get_pinmodearg_params(self):
        raise NotImplementedError

    def get_pinanalogrefarg_params(self):
        raise NotImplementedError

    def launch_device_operation(self, devid, type_, data):
        try:
            assert type_ in self.OPERATIONS
            operclass = get_operclass(type_)
        except:
            raise BoardUnknownOperation(type_.name, self.__class__.__name__)
        return operclass(self, data).launch(devid)


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
    PWM_PINS = (3, 5, 6, 9, 10, 11)

    def get_pinmodearg_params(self):
        return ((0, 1, 2), dict(INPUT=0, OUTPUT=1, INPUT_PULLUP=2))

    def get_pinanalogrefarg_params(self):
        return (range(0, 3), dict(DEFAULT=0, EXTERNAL=1, INTERNAL=2))


class BoardArduino_Pro5V(BoardArduino):

    INFO_URL = "http://arduino.cc/en/Main/ArduinoBoardProMini"
