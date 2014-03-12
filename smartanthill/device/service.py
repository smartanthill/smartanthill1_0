# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from twisted.application.service import MultiService

from smartanthill.device.device import Device
from smartanthill.exception import UnknownDeviceBoard, UnknownDeviceId
from smartanthill.log import Logger


class DeviceService(MultiService):

    def __init__(self, sas, options):
        MultiService.__init__(self)
        self.setName("device")
        self.log = Logger(self)
        self.sas = sas
        self.options = options

        self._devices = {}

    def startService(self):

        for devid, devoptions in self.options.items():
            devid = int(devid)
            assert devid > 0 and devid <= 255
            assert ("board" and "operations") in devoptions

            try:
                devobj = Device(self.sas, devid, devoptions)
                self._devices[devid] = devobj
            except UnknownDeviceBoard, e:
                self.log.error(e)

        MultiService.startService(self)
        self.log.info("Service has been started with options '%s'" %
                      self.options)

    def stopService(self):
        MultiService.stopService(self)
        self.log.info("Service has been stopped.")

    def get_device(self, id_):
        if not id_ in self._devices:
            raise UnknownDeviceId(id_)
        return self._devices[id_]


def makeService(sas, options):
    return DeviceService(sas, options)
