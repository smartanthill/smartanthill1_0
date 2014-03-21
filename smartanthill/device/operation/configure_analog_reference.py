# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from smartanthill.api.handler import APIPermission
from smartanthill.device.api import APIDeviceHandlerBase
from smartanthill.device.arg import PinAnalogRefArg
from smartanthill.device.operation.base import OperationBase, OperationType


class APIHandler(APIDeviceHandlerBase):

    PERMISSION = APIPermission.UPDATE
    KEY = "device.analogreference"
    REQUIRED_PARAMS = ("devid", "ref")

    def handle(self, data):
        return self.launch_operation(
            data['devid'], OperationType.CONFIGURE_ANALOG_REFERENCE, data)


class Operation(OperationBase):

    TYPE = OperationType.CONFIGURE_ANALOG_REFERENCE

    def process_data(self, data):
        arg = PinAnalogRefArg(*self.board.get_pinanalogrefarg_params())
        arg.set_value(data['ref'])
        return [arg.get_value()]
