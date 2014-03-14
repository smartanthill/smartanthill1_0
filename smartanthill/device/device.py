# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from smartanthill.device.board import BoardFactory
from smartanthill.exception import UnknownDeviceOperation
from smartanthill.log import Logger


class Device(object):

    def __init__(self, id_, options):
        self.log = Logger("device.%d" % id_)
        self.id_ = id_
        self.options = options
        self.operations = [o.lower() for o in self.options['operations']]
        self.board = BoardFactory.newBoard(options["board"])

    def launch_operation(self, name, *args):
        try:
            self.operations.index(name.lower())
        except ValueError:
            raise UnknownDeviceOperation(name, self.id_)
        else:
            return self.board.launch_device_operation(self.id_, name, *args)
