# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from smartanthill.api.handler import APIPermission
from smartanthill.device.api import APIDeviceHandlerBase
from smartanthill.device.arg import PinArg, PinPWMValueArg
from smartanthill.device.operation.base import OperationBase, OperationType


class APIHandler(APIDeviceHandlerBase):

    PERMISSION = APIPermission.UPDATE
    KEY = "device.analogpin"
    REQUIRED_PARAMS = ("devid", "pin[]")

    def handle(self, data):
        return self.launch_operation(data['devid'],
                                     OperationType.WRITE_ANALOG_PIN, data)


class Operation(OperationBase):

    TYPE = OperationType.WRITE_ANALOG_PIN

    def process_data(self, data):
        args = []
        for _key, _value in data.items():
            if "pin[" not in _key:
                continue
            pinarg = PinArg(*self.board.get_pwmpinarg_params())
            pinpwmarg = PinPWMValueArg()
            pinarg.set_value(_key[4:-1])
            pinpwmarg.set_value(_value)
            args += [pinarg, pinpwmarg]
        return [a.get_value() for a in args]
