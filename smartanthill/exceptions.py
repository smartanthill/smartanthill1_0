# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

class ConfigKeyError(KeyError):
    pass

class NotImplemnetedYet(Exception):
    pass

class LiteMQACKFailed(Exception):
    pass

class SATPMessageLost(Exception):
    pass

class NetworkRouterConnectFailure(Exception):
    pass
