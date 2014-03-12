# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

"""
    Channel Data Classifier
    docs/specification/network/cdc/index.html
"""


class CHANNEL_URGENT:

    PING = 0x00
    SEGMENT_ACKNOWLEDGMENT = 0x0A


class CHANNEL_BDCREQUEST:

    LIST_OPERATIONAL_STATES = 0x89
    CONFIGURE_PIN_MODE = 0x8A
    READ_DIGITAL_PIN = 0x8B
    WRITE_DIGITAL_PIN = 0x8C
    CONFIGURE_ANALOG_REFERENCE = 0x8D
    READ_ANALOG_PIN = 0x8E
