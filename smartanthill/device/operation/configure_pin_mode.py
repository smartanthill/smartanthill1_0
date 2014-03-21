# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from smartanthill.api.handler import APIPermission
from smartanthill.device.api import APIDeviceHandlerBase
from smartanthill.device.arg import PinArg, PinModeArg
from smartanthill.device.operation.base import OperationBase, OperationType


class APIHandler(APIDeviceHandlerBase):

    PERMISSION = APIPermission.UPDATE
    KEY = "device.pinmode"
    REQUIRED_PARAMS = ("devid", "pin[]")

    def handle(self, data):
        return self.launch_operation(data['devid'],
                                     OperationType.CONFIGURE_PIN_MODE, data)


class Operation(OperationBase):

    TYPE = OperationType.CONFIGURE_PIN_MODE

    def process_data(self, data):
        args = []
        for _key, _value in data.items():
            if "pin[" not in _key:
                continue
            pinarg = PinArg(*self.board.get_pinarg_params())
            pinmodearg = PinModeArg(*self.board.get_pinmodearg_params())
            pinarg.set_value(_key[4:-1])
            pinmodearg.set_value(_value)
            args += [pinarg, pinmodearg]
        return [a.get_value() for a in args]
