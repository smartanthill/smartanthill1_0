/**
 * Copyright (C) 2013-2014 Ivan Kravets <me@ikravets.com>
 * See LICENSE for details.
 */

#ifndef __ROUTER_H__
#define __ROUTER_H__

#include "platform_tools.h"
#include "configuration.h"
#include "crc.h"

/* Based on /docs/specification/network/protocols/sarp.html */
#define PROTOCOL_SOP_CODE       0x1
#define PROTOCOL_HEADER_LEN     4
#define PROTOCOL_MAXDATA_LEN    8
#define PROTOCOL_CRC_LEN        2
#define PROTOCOL_EOF_CODE       0x17

#define BUFFER_IN_LEN           16 /* The sum of PROTOCOL_* defines length */
#define BUFFER_OUT_LEN          5

#define PACKET_FLAG_SEG         0x4
#define PACKET_FLAG_FIN         0x2
#define PACKET_FLAG_ACK         0x1

#define PACKET_OUT_TIMEOUT      1000 /* In milliseconds */

typedef struct
{
    uint8_t cdc;
    uint8_t sourceId;
    uint8_t destinationId;
    uint8_t satpFlags;
    uint8_t dataLength;
    uint8_t data[8];
    crc_t crc;

} RouterPacket;

typedef struct
{
    RouterPacket rp;
    uint32_t expireTime;
    uint8_t sentNums;

} RouterPacketOutStack;

#ifdef __cplusplus
extern "C" {
#endif

void routerLoop();
inline uint8_t routerHasInPacket();
inline RouterPacket *routerGetInPacket();
void routerSendPacket(RouterPacket* outRP);
void routerAcknowledgeOutPacket(RouterPacket* outRP);

#ifdef __cplusplus
}
#endif

static void _routerOnByteReceived(uint8_t inByte);
static void _routerBufferPushByte(uint8_t inByte);
static uint8_t _routerBufferContainsPacket(uint8_t sopIndex);
static void _routerParseBufferPacket(uint8_t sopIndex);
static void _routerAcknowledgeInPacket();
static void _routerShiftOutPacketStack();
static void _routerResendOutPackets();

#endif
