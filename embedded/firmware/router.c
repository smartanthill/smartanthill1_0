/**
 * Copyright (C) Ivan Kravets <me@ikravets.com>
 * See LICENSE for details.
 */

#include "router.h"

static RouterPacket _inRP;
static uint8_t _newInRPReady = 0;
static uint8_t _inBuffer[BUFFER_IN_LEN] = {0};
static RouterPacketOutStack _outRPStack[BUFFER_OUT_LEN] = {{0}};

void routerInit()
{
    UARTInit(ROUTER_UART_SPEED);
}

void routerLoop()
{
    _newInRPReady = 0;

    if (BUFFER_OUT_LEN)
        _routerResendOutPackets();

    int16_t _rxByte;
    while (!_newInRPReady && (_rxByte = UARTReceiveByte()) != -1)
        _routerOnByteReceived(_rxByte);

    if (_newInRPReady && _inRP.destinationId == DEVICE_ID \
            && _inRP.satpFlags & PACKET_FLAG_ACK)
        _routerAcknowledgeInPacket();
}

inline uint8_t routerHasInPacket()
{
    return _newInRPReady;
}

inline RouterPacket *routerGetInPacket()
{
    return &_inRP;
}

void routerSendPacket(RouterPacket* outRP)
{
    UARTTransmitByte(PROTOCOL_SOP_CODE);
    UARTTransmitByte(outRP->cdc);
    UARTTransmitByte(outRP->sourceId);
    UARTTransmitByte(outRP->destinationId);

    uint8_t _flags = (outRP->satpFlags << 5) | outRP->dataLength;
    UARTTransmitByte(_flags);

    uint8_t i;
    for (i = 0; i < outRP->dataLength; i++)
        UARTTransmitByte(outRP->data[i]);

    /* calc CRC */
    outRP->crc = crc_update(0, &outRP->cdc, 1);
    outRP->crc = crc_update(outRP->crc, &outRP->sourceId, 1);
    outRP->crc = crc_update(outRP->crc, &outRP->destinationId, 1);
    outRP->crc = crc_update(outRP->crc, &_flags, 1);
    outRP->crc = crc_update(outRP->crc, outRP->data, outRP->dataLength);
    UARTTransmitByte(outRP->crc >> 8);
    UARTTransmitByte(outRP->crc & 0xFF);

    UARTTransmitByte(PROTOCOL_EOF_CODE);

    if (BUFFER_OUT_LEN && outRP->satpFlags & PACKET_FLAG_ACK)
    {
        /* check if this packet already in buffer */
        for (i = 0; i < BUFFER_OUT_LEN; i++)
        {
            if (&_outRPStack[i].rp == outRP)
                return;
        }

        _routerShiftOutPacketStack();
        _outRPStack[0].rp = *outRP;
        _outRPStack[0].expireTime = getTimeMillis() + PACKET_OUT_TIMEOUT;
        _outRPStack[0].sentNums = 1;
    }
}

void routerAcknowledgeOutPacket(RouterPacket* outRP)
{
    uint8_t i;
    for (i = 0; i < BUFFER_OUT_LEN; i++)
    {
        if (!_outRPStack[i].sentNums ||
            _outRPStack[i].rp.destinationId != outRP->sourceId ||
            _outRPStack[i].rp.sourceId != outRP->destinationId ||
            _outRPStack[i].rp.crc != (outRP->data[0] << 8 | outRP->data[1]))
            continue;

        _outRPStack[i].sentNums = 0;
        _outRPStack[i].expireTime = 0;
    }
}

static void _routerOnByteReceived(uint8_t inByte)
{
    _routerBufferPushByte(inByte);

    if (inByte != PROTOCOL_EOF_CODE)
        return;

    /* "-1" this is EOF length */
    uint8_t i = BUFFER_IN_LEN - 1 - PROTOCOL_CRC_LEN - PROTOCOL_HEADER_LEN;
    for (; i > 0; i--)
    {
        if (_inBuffer[i-1] != PROTOCOL_SOP_CODE)
            continue;

        if (_routerBufferContainsPacket(i - 1))
        {
            _routerParseBufferPacket(i - 1);
            _newInRPReady = 1;
            return;
        }
    }
}

static void _routerBufferPushByte(byte inByte)
{
    uint8_t i;
    for (i = 1; i < BUFFER_IN_LEN; i++)
        _inBuffer[i-1] = _inBuffer[i];

    _inBuffer[BUFFER_IN_LEN - 1] = inByte;
}

static uint8_t _routerBufferContainsPacket(uint8_t sopIndex)
{
    _inRP.dataLength = _inBuffer[sopIndex + PROTOCOL_HEADER_LEN] & 0xF;

    if (_inRP.dataLength > PROTOCOL_MAXDATA_LEN ||
        sopIndex + PROTOCOL_HEADER_LEN + _inRP.dataLength \
        + PROTOCOL_CRC_LEN + 2 != BUFFER_IN_LEN )
        return 0;

    _inRP.crc = _inBuffer[BUFFER_IN_LEN - PROTOCOL_CRC_LEN - 1] << 8;
    _inRP.crc |= _inBuffer[BUFFER_IN_LEN - PROTOCOL_CRC_LEN];

    return _inRP.crc == crc_update(
            0,
            &_inBuffer[sopIndex + 1],
            PROTOCOL_HEADER_LEN + _inRP.dataLength);
}

static void _routerParseBufferPacket(uint8_t sopIndex)
{
    /* dataLen + crc already parsed in _routerBufferContainsPacket */
    uint8_t i;
    for (i = 0; i < _inRP.dataLength; i++)
        _inRP.data[i] = _inBuffer[sopIndex + PROTOCOL_HEADER_LEN + i + 1];

    _inRP.cdc = _inBuffer[sopIndex + 1];
    _inRP.sourceId = _inBuffer[sopIndex + 2];
    _inRP.destinationId = _inBuffer[sopIndex + 3];
    _inRP.satpFlags = _inBuffer[sopIndex + 4] >> 5;
}

static void _routerAcknowledgeInPacket()
{
    RouterPacket outRP;
    outRP.cdc = 0x0A;
    outRP.sourceId = _inRP.destinationId;
    outRP.destinationId = _inRP.sourceId;
    outRP.satpFlags = PACKET_FLAG_FIN;
    outRP.dataLength = 2;
    outRP.data[0] = _inRP.crc >> 8;
    outRP.data[1] = _inRP.crc & 0xFF;

    routerSendPacket(&outRP);
}

static void _routerShiftOutPacketStack()
{
    uint8_t i;
    for (i = BUFFER_OUT_LEN-1; i > 0; i--)
        _outRPStack[i] = _outRPStack[i-1];
}

static void _routerResendOutPackets()
{
    uint32_t now = getTimeMillis();
    uint8_t i;
    for (i = 0; i < BUFFER_OUT_LEN; i++)
    {
        if (!_outRPStack[i].sentNums || _outRPStack[i].expireTime >= now)
            continue;

        _outRPStack[i].expireTime = now + \
                                (PACKET_OUT_TIMEOUT * _outRPStack[i].sentNums);
        _outRPStack[i].sentNums++;

        routerSendPacket(&_outRPStack[i].rp);
    }
}

