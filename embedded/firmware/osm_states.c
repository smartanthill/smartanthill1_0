/**
 * Copyright (C) Ivan Kravets <me@ikravets.com>
 * See LICENSE for details.
 */

#include "osm_states.h"

void osmStateAcknowledgeOutPacket()
{
    routerAcknowledgeOutPacket(routerGetInPacket());
    osm.makeTransition(IDLE_STATE);
}

void osmConfigurePinMode()
{
    RouterPacket *inPacket = routerGetInPacket();

    uint8_t i;
    for (i = 0; i < inPacket->dataLength; i+=2)
        configurePinMode(inPacket->data[i], inPacket->data[i+1]);

    osm.makeTransition(IDLE_STATE);
}

void osmStateReadDigitalPin()
{
    RouterPacket *inPacket = routerGetInPacket();
    RouterPacket outPacket;

    outPacket.cdc = 0xCA;
    outPacket.sourceId = inPacket->destinationId;
    outPacket.destinationId = inPacket->sourceId;
    outPacket.satpFlags = PACKET_FLAG_FIN | PACKET_FLAG_ACK;
    outPacket.dataLength = inPacket->dataLength;

    uint8_t i;
    for (i = 0; i < inPacket->dataLength; i++)
        outPacket.data[i] = readDigitalPin(inPacket->data[i]);

    routerSendPacket(&outPacket);

    osm.makeTransition(IDLE_STATE);
}

void osmStateWriteDigitalPin()
{
    RouterPacket *inPacket = routerGetInPacket();

    uint8_t i;
    for (i = 0; i < inPacket->dataLength; i+=2)
        writeDigitalPin(inPacket->data[i], inPacket->data[i+1]);

    osm.makeTransition(IDLE_STATE);
}
