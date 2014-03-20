/**
 * Copyright (C) Ivan Kravets <me@ikravets.com>
 * See LICENSE for details.
 */

#ifndef __OSM_STATES_H__
#define __OSM_STATES_H__

#include "osm.h"
#include "router.h"

#ifdef __cplusplus
extern "C" {
#endif

void osmStateAcknowledgeOutPacket();
void osmStateListOperations();
void osmStateConfigurePinMode();
void osmStateReadDigitalPin();
void osmStateWriteDigitalPin();
void osmStateConfigureAnalogReference();
void osmStateReadAnalogPin();
void osmStateWriteAnalogPin();

#ifdef __cplusplus
}
#endif

#endif
