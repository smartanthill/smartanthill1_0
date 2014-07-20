# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

# from twisted.internet.defer import inlineCallbacks
from twisted.python.constants import ValueConstant

from smartanthill.device.board.base import BoardFactory
from smartanthill.device.operation.base import OperationType
from smartanthill.exception import DeviceUnknownOperation
from smartanthill.log import Logger


class Device(object):

    def __init__(self, id_, options):
        self.log = Logger("device.%d" % id_)
        self.id_ = id_
        self.options = options
        self.board = BoardFactory.newBoard(options['boardId'])
        self.operations = set([OperationType.PING,
                               OperationType.LIST_OPERATIONS])

        if "operationIds" in options:
            for cdc in options['operationIds']:
                self.operations.add(OperationType.lookupByValue(cdc))

        self.log.info("Allowed operations: %s" % ([o.name for o in
                                                   self.operations]))

    def get_name(self):
        return self.options.get(
            "name", "Device #%d, %s" % (self.id_, self.board.get_name()))

    # @inlineCallbacks
    # def verify_operations(self):
    #     result = yield self.launch_operation(OperationType.LIST_OPERATIONS)
    #     for cdc in result:
    #         self.operations.add(OperationType.lookupByValue(cdc))
    #     self.operations = frozenset(self.operations)

    def launch_operation(self, type_, data=None):
        assert isinstance(type_, ValueConstant)
        if type_ in self.operations:
            return self.board.launch_operation(self.id_, type_, data)
        raise DeviceUnknownOperation(type_.name, self.id_)
