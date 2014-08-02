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
#ifdef OPERTYPE_LIST_OPERATIONS
    {OPERTYPE_LIST_OPERATIONS, &osmStateListOperations},
#endif

#ifdef OPERTYPE_CONFIGURE_PIN_MODE
    {OPERTYPE_CONFIGURE_PIN_MODE, &osmStateConfigurePinMode},
#endif

#ifdef OPERTYPE_READ_DIGITAL_PIN
    {OPERTYPE_READ_DIGITAL_PIN, &osmStateReadDigitalPin},
#endif

#ifdef OPERTYPE_WRITE_DIGITAL_PIN
    {OPERTYPE_WRITE_DIGITAL_PIN, &osmStateWriteDigitalPin},
#endif

#ifdef OPERTYPE_CONFIGURE_ANALOG_REFERENCE
    {OPERTYPE_CONFIGURE_ANALOG_REFERENCE, &osmStateConfigureAnalogReference},
#endif

#ifdef OPERTYPE_READ_ANALOG_PIN
    {OPERTYPE_READ_ANALOG_PIN, &osmStateReadAnalogPin},
#endif

#ifdef OPERTYPE_WRITE_ANALOG_PIN
    {OPERTYPE_WRITE_ANALOG_PIN, &osmStateWriteAnalogPin},
#endif

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

void _osmMakeTransition(const OperationalState* newState)
{
    osm.curState = newState;
}

void _osmUpdateState()
{
    if (osm.curState)
        osm.curState->update();
}

const OperationalState* _osmFindStateByCDC(uint8_t cdc)
{
    uint8_t i;
    for (i = 0; i < OSM_STATE_NUMS; i++)
    {
        if (osmStates[i].cdc == cdc)
            return &osmStates[i];
    }
    return IDLE_STATE;
}
