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

void osmStateConfigurePinMode()
{
    RouterPacket *inPacket = routerGetInPacket();
    RouterPacket outPacket;
    outPacket.cdc = 0xCA;
    outPacket.source = inPacket->destination;
    outPacket.destination = inPacket->source;
    outPacket.satpFlags = inPacket->satpFlags;
    outPacket.dataLength = 0;

    static uint8_t prevLowestByte = 0;  /* The lowest byte from previous Packet */
    uint8_t i = 0;
    uint8_t pin = 0;

    if (inPacket->satpFlags & SATP_FLAG_SEG)
    {
        /* reuse segment order */
        outPacket.data[0] = inPacket->data[0];
        outPacket.dataLength++;

        if (inPacket->dataLength == PACKET_MAXDATA_LEN)
        {
            i = 1;
            prevLowestByte = 0;
        }
    }

    if (inPacket->dataLength >= i+2)
    {
        for (; i < inPacket->dataLength-1; i+=2)
        {
            if (i == 0 && prevLowestByte)
                pin = prevLowestByte;
            else
                pin = inPacket->data[i];

            configurePinMode(pin, inPacket->data[i+1]);

            /* collects result pins */
            outPacket.data[outPacket.dataLength] = pin;
            outPacket.dataLength++;
        }
    }

    if (inPacket->satpFlags & SATP_FLAG_SEG &&
            inPacket->dataLength == PACKET_MAXDATA_LEN)
        prevLowestByte = inPacket->data[PACKET_MAXDATA_LEN-1];

    routerSendPacket(&outPacket);
    osm.makeTransition(IDLE_STATE);
}

void osmStateReadDigitalPin()
{
    RouterPacket *inPacket = routerGetInPacket();

    RouterPacket outPacket;
    outPacket.cdc = 0xCB;
    outPacket.source = inPacket->destination;
    outPacket.destination = inPacket->source;
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
    RouterPacket outPacket;
    outPacket.cdc = 0xCC;
    outPacket.source = inPacket->destination;
    outPacket.destination = inPacket->source;
    outPacket.satpFlags = inPacket->satpFlags;
    outPacket.dataLength = 0;

    static uint8_t prevLowestByte = 0;  /* The lowest byte from previous Packet */
    uint8_t i = 0;
    uint8_t pin = 0;

    if (inPacket->satpFlags & SATP_FLAG_SEG)
    {
        /* reuse segment order */
        outPacket.data[0] = inPacket->data[0];
        outPacket.dataLength++;

        if (inPacket->dataLength == PACKET_MAXDATA_LEN)
        {
            i = 1;
            prevLowestByte = 0;
        }
    }

    if (inPacket->dataLength >= i+2)
    {
        for (; i < inPacket->dataLength-1; i+=2)
        {
            if (i == 0 && prevLowestByte)
                pin = prevLowestByte;
            else
                pin = inPacket->data[i];

            writeDigitalPin(pin, inPacket->data[i+1]);

            /* collects result pins */
            outPacket.data[outPacket.dataLength] = pin;
            outPacket.dataLength++;
        }
    }

    if (inPacket->satpFlags & SATP_FLAG_SEG &&
            inPacket->dataLength == PACKET_MAXDATA_LEN)
        prevLowestByte = inPacket->data[PACKET_MAXDATA_LEN-1];

    routerSendPacket(&outPacket);
    osm.makeTransition(IDLE_STATE);
}
