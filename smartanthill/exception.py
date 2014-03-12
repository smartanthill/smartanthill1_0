# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.


class SABaseException(Exception):

    message = None

    def __str__(self):
        if self.message:
            return self.message % self.args
        else:
            return Exception.__str__(self)


class ConfigKeyError(SABaseException, KeyError):

    message = "Invalid config data path '%s'"


class NotImplemnetedYet(SABaseException):
    pass


class LiteMQACKFailed(SABaseException):
    pass


class SATPMessageLost(SABaseException):

    message = "Message has been lost: %s"


class NetworkRouterConnectFailure(SABaseException):

    message = "Couldn't connect to router with options=%s"


class UnknownBoardOperation(SABaseException):

    message = "Unknown operation '%s' for %s"


class UnknownDeviceId(SABaseException):

    message = "Unknown device with ID=%d"


class UnknownDeviceBoard(SABaseException):

    message = "Unknown device board '%s'"


class UnknownDeviceOperation(SABaseException):

    message = "Unknown operation '%s' for device #%d"


class OperArgInvalid(SABaseException):

    message = "%s%s: Invalid value '%s'"


class OperArgNumsExceeded(SABaseException):

    message = "Took %d arguments(max=%d) for '%s' operation"


