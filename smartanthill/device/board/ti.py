# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from smartanthill.device.board.base import BoardBase


class BoardTIMSP430G2Base(BoardBase):
    VENDOR = "Texas Instruments"

    PLATFORMIO_PLATFORM = "timsp430"
    PLATFORMIO_FRAMEWORK = "energia"

    PINS = range(2, 16) + [18, 19]
    PINS_ALIAS = dict(
        # Labels
        P1_0=2,
        P1_1=3,
        P1_2=4,
        P1_3=5,
        P1_4=6,
        P1_5=7,
        P2_0=8,
        P2_1=9,
        P2_2=10,
        P2_3=11,
        P2_4=12,
        P2_5=13,
        P1_6=14,
        P1_7=15,
        P2_7=18,
        P2_6=19,

        # Serial
        RX=3, TX=4,

        # SPI
        SS=8, MOSI=15, MISO=14, SCK=7,

        # I2C
        SDA=14, SCL=15,

        # Analog
        A0=2, A1=3, A2=4, A3=5, A4=6, A5=7, A6=14, A7=15,

        # LEDs
        LED_BUILTIN=2,
        RED_LED=2,
        GREEN_LED=14,

        # Miscellaneous
        PUSH2=5
    )
    ANALOG_PINS = (2, 3, 4, 5, 6, 7, 14, 15)
    PWM_PINS = (4, 9, 10, 12, 13, 14, 19)
    EXTINT_PINS = range(2, 16) + [18, 19]

    def get_pinmodearg_params(self):
        return ((0, 1, 2, 4), dict(INPUT=0, OUTPUT=1, INPUT_PULLUP=2,
                                   INPUT_PULLDOWN=4))

    def get_pinanalogrefarg_params(self):
        return ((0, 1, 2, 3), dict(DEFAULT=0, EXTERNAL=1, INTERNAL1V5=2,
                                   INTERNAL2V5=3))


class Board_TI_LPmsp430g2231(BoardTIMSP430G2Base):

    NAME = "TI LaunchPad MSP430 (msp430g2231)"
    PLATFORMIO_BOARD = "lpmsp430g2231"

    def __init__(self):
        self.PINS_ALIAS['MOSI'] = 14
        self.PINS_ALIAS['MISO'] = 15


class Board_TI_LPmsp430g2452(BoardTIMSP430G2Base):

    NAME = "TI LaunchPad MSP430 (msp430g2452)"
    PLATFORMIO_BOARD = "lpmsp430g2452"

    PWM_PINS = (4, 14)

    def __init__(self):
        self.PINS_ALIAS['MOSI'] = 14
        self.PINS_ALIAS['MISO'] = 15


class Board_TI_LPmsp430g2553(BoardTIMSP430G2Base):

    NAME = "TI LaunchPad MSP430 (msp430g2553)"
    PLATFORMIO_BOARD = "lpmsp430g2553"


class Board_TI_FPmsp430fr5739(BoardTIMSP430G2Base):

    NAME = "TI FraunchPad MSP430 (msp430fr5739)"
    PLATFORMIO_BOARD = "lpmsp430fr5739"


class Board_TI_LPmsp430f5529(BoardTIMSP430G2Base):

    NAME = "TI LaunchPad MSP430 (msp430f5529, 16MHz)"
    PLATFORMIO_BOARD = "lpmsp430f5529"


class Board_TI_LPmsp430f5529_25(BoardTIMSP430G2Base):

    NAME = "TI LaunchPad MSP430 (msp430f5529, 25MHz)"
    PLATFORMIO_BOARD = "lpmsp430f5529_25"


class Board_TI_LPmsp430fr5969(BoardTIMSP430G2Base):

    NAME = "TI LaunchPad MSP430 (msp430fr5969)"
    PLATFORMIO_BOARD = "lpmsp430fr5969"
