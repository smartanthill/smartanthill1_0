# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from twisted.internet.defer import inlineCallbacks, returnValue

from smartanthill.api.handler import APIPermission
from smartanthill.device.api import APIDeviceHandlerBase
from smartanthill.device.operation.base import OperationBase, OperationType


class APIHandler(APIDeviceHandlerBase):

    PERMISSION = APIPermission.GET
    KEY = "device.operations"
    REQUIRED_PARAMS = ("devid",)

    @inlineCallbacks
    def handle(self, data):
        result = yield self.launch_operation(
            data['devid'], OperationType.LIST_OPERATIONS)
        operations = {OperationType.PING.value: OperationType.PING.name}
        for cdc in result:
            _ot = OperationType.lookupByValue(cdc)
            operations[_ot.value] = _ot.name
        returnValue(operations)


class Operation(OperationBase):

    TYPE = OperationType.LIST_OPERATIONS
