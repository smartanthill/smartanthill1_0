# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from smartanthill.api.handler import APIPermission
from smartanthill.device.api import APIDeviceHandlerBase
from smartanthill.device.arg import PinArg
from smartanthill.device.operation.base import OperationBase, OperationType


class APIHandler(APIDeviceHandlerBase):

    PERMISSION = APIPermission.GET
    KEY = "device.digitalpin"
    REQUIRED_PARAMS = ("devid", "pin")

    def handle(self, data):
        return self.launch_operation(data['devid'],
                                     OperationType.READ_DIGITAL_PIN, data)


class Operation(OperationBase):

    TYPE = OperationType.READ_DIGITAL_PIN

    def process_data(self, data):
        args = []
        pins = data['pin'] if isinstance(data['pin'], list) else (data['pin'],)
        for pin in pins:
            pinarg = PinArg(*self.board.get_pinarg_params())
            pinarg.set_value(pin)
            args.append(pinarg)
        return [a.get_value() for a in args]
