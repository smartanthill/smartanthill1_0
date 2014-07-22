# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from os import listdir

from twisted.python.reflect import namedModule
from twisted.python.util import sibpath

from smartanthill.device.board.base import BoardBase
from smartanthill.device.device import Device
from smartanthill.exception import (BoardUnknownId, DeviceUnknownBoard,
                                    DeviceUnknownId)
from smartanthill.service import SAMultiService


class DeviceService(SAMultiService):

    def __init__(self, name, options):
        SAMultiService.__init__(self, name, options)
        self._devices = {}

    def startService(self):
        for devid, devoptions in self.options.get("devices", {}).items():
            devid = int(devid)
            assert 0 < devid <= 255
            assert "boardId" in devoptions
            assert "network" in devoptions

            try:
                self._devices[devid] = Device(devid, devoptions)
            except DeviceUnknownBoard, e:
                self.log.error(e)

        SAMultiService.startService(self)

    def get_devices(self):
        return self._devices

    def get_device(self, id_):
        if id_ not in self._devices:
            raise DeviceUnknownId(id_)
        return self._devices[id_]

    @staticmethod
    def get_boards():
        boards = {}
        for d in listdir(sibpath(__file__, "board")):
            if d.startswith("__") or not d.endswith(".py"):
                continue
            module = namedModule("smartanthill.device.board.%s" % d[:-3])
            for clsname in dir(module):
                if not clsname.startswith("Board_"):
                    continue
                obj = getattr(module, clsname)()
                assert isinstance(obj, BoardBase)
                boards[obj.get_id()] = obj
        return boards

    @staticmethod
    def get_board(id_):
        try:
            return DeviceService.get_boards()[id_]
        except KeyError:
            raise BoardUnknownId(id_)


def makeService(name, options):
    return DeviceService(name, options)
