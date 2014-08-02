/**
 * Copyright (C) Ivan Kravets <me@ikravets.com>
 * See LICENSE for details.
 */

#ifndef __PLATFORM_TOOLS_H__
#define __PLATFORM_TOOLS_H__

#ifdef ARDUINO
#include "Arduino.h"
#endif

#ifdef __cplusplus
extern "C" {
#endif

void UARTInit(const uint16_t speed);
void UARTTransmitByte(uint8_t _byte);
int16_t UARTReceiveByte();
void UARTPrintln(const char *data);
uint32_t getTimeMillis();
void configurePinMode(uint8_t pinNum, uint8_t value);
uint8_t readDigitalPin(uint8_t pinNum);
void writeDigitalPin(uint8_t pinNum, uint8_t value);
void configureAnalogReference(uint8_t mode);
uint16_t readAnalogPin(uint8_t pinNum);
void writeAnalogPin(uint8_t pinNum, uint8_t value);

#ifdef __cplusplus
}
#endif

#endif
