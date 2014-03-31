# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from smartanthill.api.handler import APIPermission
from smartanthill.device.api import APIDeviceHandlerBase
from smartanthill.device.arg import PinArg
from smartanthill.device.operation.base import OperationBase, OperationType


class APIHandler(APIDeviceHandlerBase):

    PERMISSION = APIPermission.GET
    KEY = "device.analogpin"
    REQUIRED_PARAMS = ("devid", "pin")

    def handle(self, data):
        return self.launch_operation(data['devid'],
                                     OperationType.READ_ANALOG_PIN, data)


class Operation(OperationBase):

    TYPE = OperationType.READ_ANALOG_PIN

    def process_data(self, data):
        args = []
        pins = data['pin'] if isinstance(data['pin'], list) else (data['pin'],)
        for pin in pins:
            pinarg = PinArg(*self.board.get_analogpinarg_params())
            pinarg.set_value(pin)
            args.append(pinarg)
        return [a.get_value() for a in args]

    def on_result(self, result):
        assert len(result) % 2 == 0
        newres = []
        while result:
            msb, lsb = result[0:2]
            del result[0:2]
            newres.append(msb << 8 | lsb)
        return newres
