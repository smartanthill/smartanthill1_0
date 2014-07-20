# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.


class SABaseException(Exception):

    MESSAGE = None

    def __str__(self):  # pragma: no cover
        if self.MESSAGE:
            return self.MESSAGE % self.args
        else:
            return Exception.__str__(self)


class ConfigKeyError(SABaseException, KeyError):

    MESSAGE = "Invalid config data path '%s'"


class NotImplemnetedYet(SABaseException):
    pass


class LiteMQACKFailed(SABaseException):
    pass


class LiteMQResendFailed(SABaseException):
    pass


class NetworkSATPMessageLost(SABaseException):

    MESSAGE = "Message has been lost: %s"


class NetworkRouterConnectFailure(SABaseException):

    MESSAGE = "Couldn't connect to router with options=%s"


class BoardUnknownId(SABaseException):

    MESSAGE = "Unknown board with ID=%s"


class BoardUnknownOperation(SABaseException):

    MESSAGE = "Unknown operation '%s' for %s"


class DeviceUnknownId(SABaseException):

    MESSAGE = "Unknown device with ID=%s"


class DeviceUnknownBoard(SABaseException):

    MESSAGE = "Unknown device board '%s'"


class DeviceUnknownOperation(SABaseException):

    MESSAGE = "Unknown operation '%s' for device #%d"


class DeviceNotResponding(SABaseException):

    MESSAGE = "Device #%d is not responding (tried %s times)"


class OperArgInvalid(SABaseException):

    MESSAGE = "%s%s: Invalid value '%s'"


class APIUnknownRequest(SABaseException):

    MESSAGE = "Unknown '%s' action with key '%s'"


class APIRequiredParams(SABaseException):

    MESSAGE = "These parameters '%s' are required for '%s' action"


class WebRouterMatchNotFound(SABaseException):

    MESSAGE = "Could not find any routes by '%s %s'"
