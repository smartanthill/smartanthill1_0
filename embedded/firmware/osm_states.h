/**
 * Copyright (C) 2013-2014 Ivan Kravets <me@ikravets.com>
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
void osmConfigurePinMode();
void osmStateReadDigitalPin();
void osmStateWriteDigitalPin();

#ifdef __cplusplus
}
#endif

#endif
