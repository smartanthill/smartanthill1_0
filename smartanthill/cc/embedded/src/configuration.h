/**
 * Copyright (C) Ivan Kravets <me@ikravets.com>
 * See LICENSE for details.
 */

/* The content of this file will be replaced by real dynamic data from main
SmartAnthill System */

#ifndef __CONFIGURATION__
#define __CONFIGURATION__

#define DEVICE_ID                            128

#define OPERTYPE_PING                        0x00
#define OPERTYPE_LIST_OPERATIONS             0x89
#define OPERTYPE_CONFIGURE_PIN_MODE          0x8A
#define OPERTYPE_READ_DIGITAL_PIN            0x8B
#define OPERTYPE_WRITE_DIGITAL_PIN           0x8C
#define OPERTYPE_CONFIGURE_ANALOG_REFERENCE  0x8D
#define OPERTYPE_READ_ANALOG_PIN             0x8E
#define OPERTYPE_WRITE_ANALOG_PIN            0x8F

#define ROUTER_UART_SPEED                    9600

#endif
