/**
 * Copyright (C) 2013-2014 Ivan Kravets <me@ikravets.com>
 * See LICENSE for details.
 */

#include "osm.h"

OperationalStateMachine osm = {
    NULL,
    &_osmMakeTransition,
    &_osmUpdateState,
    &_osmFindStateByCDC
};

static const OperationalState osmStates[] =
{

#ifdef OSM_STATE_CONFIGUREPINMODE
    {OSM_STATE_CONFIGUREPINMODE, &osmConfigurePinMode},
#endif

#ifdef OSM_STATE_READDIGITALPIN
    {OSM_STATE_READDIGITALPIN, &osmStateReadDigitalPin},
#endif

#ifdef OSM_STATE_WRITEDIGITALPIN
    {OSM_STATE_WRITEDIGITALPIN, &osmStateWriteDigitalPin},
#endif

    {0x0A, &osmStateAcknowledgeOutPacket}
};

static const uint8_t OSM_STATE_NUMS = sizeof osmStates / sizeof osmStates[0];


static void _osmMakeTransition(const OperationalState* newState)
{
    osm.curState = newState;
}

static void _osmUpdateState()
{
    if (osm.curState)
        osm.curState->update();
}

static const OperationalState* _osmFindStateByCDC(uint8_t cdc)
{
    uint8_t i;
    for (i = 0; i < OSM_STATE_NUMS; i++)
    {
        if (osmStates[i].cdc == cdc)
            return &osmStates[i];
    }
    return IDLE_STATE;
}
