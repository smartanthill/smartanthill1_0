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

    static uint8_t prevLowestByte = 0;  /* The lowest byte from previous Packet */
    uint8_t i = 0;

    if (inPacket->satpFlags & SATP_FLAG_SEG &&
            inPacket->dataLength == PACKET_MAXDATA_LEN)
    {
        i = 1;
        prevLowestByte = 0;
    }

    if (inPacket->dataLength >= i+2)
    {
        for (; i < inPacket->dataLength-1; i+=2)
        {
            if (i == 0 && prevLowestByte)
                configurePinMode(prevLowestByte, inPacket->data[i+1]);
            else
                configurePinMode(inPacket->data[i], inPacket->data[i+1]);
        }
    }

    if (inPacket->satpFlags & SATP_FLAG_SEG &&
            inPacket->dataLength == PACKET_MAXDATA_LEN)
        prevLowestByte = inPacket->data[PACKET_MAXDATA_LEN-1];

    osm.makeTransition(IDLE_STATE);
}

void osmStateReadDigitalPin()
{
    RouterPacket *inPacket = routerGetInPacket();
    RouterPacket outPacket;

    outPacket.cdc = 0xCB;
    outPacket.sourceId = inPacket->destinationId;
    outPacket.destinationId = inPacket->sourceId;
    outPacket.satpFlags = SATP_FLAG_FIN | SATP_FLAG_ACK;
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

    static uint8_t prevLowestByte = 0;  /* The lowest byte from previous Packet */
    uint8_t i = 0;

    if (inPacket->satpFlags & SATP_FLAG_SEG &&
            inPacket->dataLength == PACKET_MAXDATA_LEN)
    {
        i = 1;
        prevLowestByte = 0;
    }

    if (inPacket->dataLength >= i+2)
    {
        for (; i < inPacket->dataLength-1; i+=2)
        {
            if (i == 0 && prevLowestByte)
                writeDigitalPin(prevLowestByte, inPacket->data[i+1]);
            else
                writeDigitalPin(inPacket->data[i], inPacket->data[i+1]);
        }
    }

    if (inPacket->satpFlags & SATP_FLAG_SEG &&
            inPacket->dataLength == PACKET_MAXDATA_LEN)
        prevLowestByte = inPacket->data[PACKET_MAXDATA_LEN-1];

    osm.makeTransition(IDLE_STATE);
}
