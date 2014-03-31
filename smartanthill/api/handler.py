# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from twisted.python.constants import FlagConstant, Flags


class APIPermission(Flags):

    GET = FlagConstant()
    ADD = FlagConstant()
    UPDATE = FlagConstant()
    DELETE = FlagConstant()


class APIHandlerBase(object):

    PERMISSION = None
    KEY = None
    REQUIRED_PARAMS = None

    def __init__(self, action, request_key):
        self.action = action
        self.request_key = request_key

    def match(self):
        return self.action & self.PERMISSION and self.request_key == self.KEY

    def check_params(self, params):
        if not self.REQUIRED_PARAMS:
            return True
        params = [s if "[" not in s else s[:s.find("[")]+"[]" for s in params]
        return set(self.REQUIRED_PARAMS) <= set(params)

    def handle(self, data):
        raise NotImplementedError
