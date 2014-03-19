# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from smartanthill.device.device import Device
from smartanthill.exception import DeviceUnknownBoard, DeviceUnknownId
from smartanthill.service import SAMultiService


class DeviceService(SAMultiService):

    def __init__(self, name, options):
        SAMultiService.__init__(self, name, options)
        self._devices = {}

    def startService(self):

        for devid, devoptions in self.options.items():
            devid = int(devid)
            assert 0 < devid <= 255
            assert ("board" and "operations") in devoptions

            try:
                devobj = Device(devid, devoptions)
                self._devices[devid] = devobj
            except DeviceUnknownBoard, e:
                self.log.error(e)

        SAMultiService.startService(self)

    def get_device(self, id_):
        if not id_ in self._devices:
            raise DeviceUnknownId(id_)
        return self._devices[id_]


def makeService(name, options):
    return DeviceService(name, options)
