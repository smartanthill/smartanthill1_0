# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

"""
Channel Data Classifier
docs/specification/network/cdc/index.html
"""

from twisted.python.constants import ValueConstant, Values


class CHANNEL_URGENT(Values):

    PING = ValueConstant(0x00)
    SEGMENT_ACKNOWLEDGMENT = ValueConstant(0x0A)


class CHANNEL_BDCREQUEST(Values):

    LIST_OPERATIONS = ValueConstant(0x89)
    CONFIGURE_PIN_MODE = ValueConstant(0x8A)
    READ_DIGITAL_PIN = ValueConstant(0x8B)
    WRITE_DIGITAL_PIN = ValueConstant(0x8C)
    CONFIGURE_ANALOG_REFERENCE = ValueConstant(0x8D)
    READ_ANALOG_PIN = ValueConstant(0x8E)
    WRITE_ANALOG_PIN = ValueConstant(0x8F)
