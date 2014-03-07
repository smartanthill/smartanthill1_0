/**
 * Copyright (C) Ivan Kravets <me@ikravets.com>
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
    {OSM_STATE_CONFIGUREPINMODE, &osmStateConfigurePinMode},
#endif

#ifdef OSM_STATE_READDIGITALPIN
    {OSM_STATE_READDIGITALPIN, &osmStateReadDigitalPin},
#endif

#ifdef OSM_STATE_WRITEDIGITALPIN
    {OSM_STATE_WRITEDIGITALPIN, &osmStateWriteDigitalPin},
#endif

#ifdef OSM_STATE_CONFIGUREANALOGREFERENCE
    {OSM_STATE_CONFIGUREANALOGREFERENCE, &osmStateConfigureAnalogReference},
#endif

#ifdef OSM_STATE_READANALOGPIN
    {OSM_STATE_READANALOGPIN, &osmStateReadAnalogPin},
#endif

#ifdef OSM_STATE_WRITEANALOGPIN
    {OSM_STATE_WRITEANALOGPIN, &osmStateWriteAnalogPin},
#endif

    {0x89, &osmStateListOperationalStates},
    {0x0A, &osmStateAcknowledgeOutPacket}
};

static const uint8_t OSM_STATE_NUMS = sizeof osmStates / sizeof osmStates[0];

uint8_t osmGetStateNums()
{
    return OSM_STATE_NUMS;
}

uint8_t osmGetStateCDCByIndex(uint8_t index)
{
    return index < OSM_STATE_NUMS? osmStates[index].cdc : 0;
}

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
