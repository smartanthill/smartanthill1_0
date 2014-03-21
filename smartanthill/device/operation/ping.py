# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from time import time

from smartanthill.api.handler import APIPermission
from smartanthill.device.api import APIDeviceHandlerBase
from smartanthill.device.operation.base import OperationBase, OperationType


class APIHandler(APIDeviceHandlerBase):

    PERMISSION = APIPermission.GET
    KEY = "device.ping"
    REQUIRED_PARAMS = ("devid",)

    def handle(self, data):
        return self.launch_operation(data['devid'], OperationType.PING)


class Operation(OperationBase):

    TYPE = OperationType.PING

    def __init__(self, board, data):
        OperationBase.__init__(self, board, data)
        self._start = time()

    def on_result(self, result):
        return time() - self._start
