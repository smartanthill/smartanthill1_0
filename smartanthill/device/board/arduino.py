# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from smartanthill.device.board.base import BoardBase


class BoardArduinoBase(BoardBase):

    VENDOR = "Arduino"

    PLATFORMIO_PLATFORM = "atmelavr"
    PLATFORMIO_FRAMEWORK = "arduino"

    PINS = range(0, 22)  # list from 0 to 21 (not 22)
    PINS_ALIAS = dict(
        # Serial
        RX=0, TX=1,

        # SPI
        SS=10, MOSI=11, MISO=12, SCK=13,

        # I2C
        SDA=18, SCL=19,

        # Analog
        A0=14, A1=15, A2=16, A3=17, A4=18, A5=19, A6=20, A7=21,

        # LEDs
        LED_BUILTIN=13
    )
    ANALOG_PINS = range(14, 22)
    PWM_PINS = (3, 5, 6, 9, 10, 11)
    EXTINT_PINS = (2, 3)

    def get_pinmodearg_params(self):
        return ((0, 1, 2), dict(INPUT=0, OUTPUT=1, INPUT_PULLUP=2))

    def get_pinanalogrefarg_params(self):
        return ((0, 1, 2), dict(DEFAULT=0, EXTERNAL=1, INTERNAL=2))


class Board_Arduino_DiecimilaATmega168(BoardArduinoBase):

    NAME = "Arduino Duemilanove or Diecimila (ATmega168)"
    PLATFORMIO_BOARD = "diecimilaatmega168"
    ANALOG_PINS = range(14, 20)


class Board_Arduino_DiecimilaATmega328(BoardArduinoBase):

    NAME = "Arduino Duemilanove or Diecimila (ATmega328)"
    PLATFORMIO_BOARD = "diecimilaatmega328"
    ANALOG_PINS = range(14, 20)


class Board_Arduino_Fio(BoardArduinoBase):

    NAME = "Arduino Fio"
    PLATFORMIO_BOARD = "fio"


class Board_Arduino_Leonardo(BoardArduinoBase):

    NAME = "Arduino Leonardo"
    PLATFORMIO_BOARD = "leonardo"

    PINS = range(0, 20)
    PINS_ALIAS = dict(
        # Serial
        RX=0, TX=1,

        # I2C
        SDA=2, SCL=3,

        # Analog
        A0=14, A1=15, A2=16, A3=17, A4=18, A5=19, A6=4, A7=6, A8=8, A9=9,
        A10=10, A11=12,

        # LEDs
        LED_BUILTIN=13
    )
    ANALOG_PINS = (14, 15, 16, 17, 18, 19, 4, 6, 8, 8, 10, 12)
    PWM_PINS = (3, 5, 6, 9, 10, 11, 13)
    EXTINT_PINS = (0, 1, 2, 3, 7)


class Board_Arduino_LilyPadUSB(BoardArduinoBase):

    NAME = "Arduino LilyPad USB"
    PLATFORMIO_BOARD = "LilyPadUSB"


class Board_Arduino_LilyPadATmega168(BoardArduinoBase):

    NAME = "Arduino LilyPad (ATmega168)"
    PLATFORMIO_BOARD = "lilypadatmega168"


class Board_Arduino_LilyPadATmega328(BoardArduinoBase):

    NAME = "Arduino LilyPad (ATmega328)"
    PLATFORMIO_BOARD = "lilypadatmega328"


class BoardArduinoMegaBase(BoardArduinoBase):

    PINS = range(0, 70)
    PINS_ALIAS = dict(
        # Serial
        RX=0, TX=1,
        RX0=0, TX0=1, RX1=19, TX1=18, RX2=17, TX2=16, RX3=15, TX3=14,

        # SPI
        SS=53, MOSI=51, MISO=50, SCK=52,

        # I2C
        SDA=20, SCL=21,

        # Analog
        A0=54, A1=55, A2=56, A3=57, A4=58, A5=59, A6=60, A7=61, A8=62, A9=63,
        A10=64, A11=65, A12=66, A13=67, A14=68, A15=69,

        # LEDs
        LED_BUILTIN=13
    )
    ANALOG_PINS = range(54, 70)
    PWM_PINS = range(2, 14) + range(44, 47)
    EXTINT_PINS = (2, 3, 18, 19, 20, 21)


class Board_Arduino_MegaATmega1280(BoardArduinoMegaBase):

    NAME = "Arduino Mega (ATmega1280)"
    PLATFORMIO_BOARD = "megaatmega1280"


class Board_Arduino_MegaATmega2560(BoardArduinoMegaBase):

    NAME = "Arduino Mega (ATmega2560)"
    PLATFORMIO_BOARD = "megaatmega2560"


class Board_Arduino_MegaADK(BoardArduinoMegaBase):

    NAME = "Arduino Mega ADK"
    PLATFORMIO_BOARD = "megaADK"


class Board_Arduino_Micro(BoardArduinoBase):

    NAME = "Arduino Micro"
    PLATFORMIO_BOARD = "micro"

    PINS = range(0, 20)
    PINS_ALIAS = dict(
        # Serial
        RX=0, TX=1,

        # I2C
        SDA=2, SCL=3,

        # Analog
        A0=14, A1=15, A2=16, A3=17, A4=18, A5=19, A6=4, A7=6, A8=8, A9=9,
        A10=10, A11=12,

        # LEDs
        LED_BUILTIN=13
    )
    ANALOG_PINS = (14, 15, 16, 17, 18, 19, 4, 6, 8, 8, 10, 12)
    PWM_PINS = (3, 5, 6, 9, 10, 11, 13)
    EXTINT_PINS = (0, 1, 2, 3)


class Board_Arduino_MiniATmega168(BoardArduinoBase):

    NAME = "Arduino Mini (ATmega168)"
    PLATFORMIO_BOARD = "miniatmega168"


class Board_Arduino_MiniATmega328(BoardArduinoBase):

    NAME = "Arduino Mini (ATmega328)"
    PLATFORMIO_BOARD = "miniatmega328"


class Board_Arduino_NanoATmega168(BoardArduinoBase):

    NAME = "Arduino Nano (ATmega168)"
    PLATFORMIO_BOARD = "nanoatmega168"


class Board_Arduino_NanoATmega328(BoardArduinoBase):

    NAME = "Arduino Nano (ATmega328)"
    PLATFORMIO_BOARD = "nanoatmega328"


class Board_Arduino_Pro8MHzATmega168(BoardArduinoBase):

    NAME = "Arduino Pro or Pro Mini (ATmega168, 3.3V, 8MHz)"
    PLATFORMIO_BOARD = "pro8MHzatmega168"


class Board_Arduino_Pro16MHzATmega168(BoardArduinoBase):

    NAME = "Arduino Pro or Pro Mini (ATmega168, 5V, 16MHz)"
    PLATFORMIO_BOARD = "pro16MHzatmega168"


class Board_Arduino_Pro8MHzATmega328(BoardArduinoBase):

    NAME = "Arduino Pro or Pro Mini (ATmega328, 3.3V, 8MHz)"
    PLATFORMIO_BOARD = "pro8MHzatmega328"


class Board_Arduino_Pro16MHzATmega328(BoardArduinoBase):

    NAME = "Arduino Pro or Pro Mini (ATmega328, 5V, 16MHz)"
    PLATFORMIO_BOARD = "pro16MHzatmega328"


class Board_Arduino_Uno(BoardArduinoBase):

    NAME = "Arduino Uno"
    PLATFORMIO_BOARD = "uno"
    ANALOG_PINS = range(14, 20)
