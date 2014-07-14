# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from twisted.python.reflect import namedObject

from smartanthill.api.handler import APIHandlerBase
from smartanthill.device.arg import DeviceIDArg
from smartanthill.device.operation.base import OperationType
from smartanthill.util import get_service_named


class APIDeviceHandlerBase(APIHandlerBase):  # pylint: disable=W0223

    @staticmethod
    def launch_operation(devid, type_, data=None):
        arg = DeviceIDArg()
        arg.set_value(devid)
        devid = arg.get_value()
        device = get_service_named("device")
        return device.get_device(devid).launch_operation(type_, data)


def get_handlers():
    handlers = []
    for c in OperationType.iterconstants():
        try:
            handler = namedObject(
                "smartanthill.device.operation.%s.APIHandler" % c.name.lower())
            handlers.append(handler)
        except AttributeError:
            continue
    return handlers
