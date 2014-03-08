# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from struct import pack

from twisted.internet import protocol, reactor
from twisted.internet.defer import Deferred
from twisted.python.failure import Failure

from smartanthill.exceptions import SATPMessageLost
from smartanthill.network.cdc import CHANNEL_URGENT
from smartanthill.util import calc_crc16


class ControlProtocol(protocol.Protocol):

    def client_message_received(self, message):
        pass

    def send_client_message(self, message):
        defmessage = dict(ack=False, ttl=1, data=[])
        defmessage.update(message)
        message = defmessage

        assert ("cdc" in message and "source" in message and "destination" in
                message)
        assert (message['ttl'] and message['ttl'] <= 15,
                "TTL should be between 1-15")
        assert len(message['data']) <= 1792

        flagsandlen = 0x80 if message["ack"] else 0
        flagsandlen |= (message["ttl"]) << 3
        flagsandlen |= len(message['data']) >> 8  # high 3 bits
        rawmessage = pack("BBBBB", message["cdc"], message["source"],
                          message["destination"], flagsandlen,
                          len(message['data']) & 0xF)
        if len(message["data"]):
            rawmessage += pack("B"*len(message["data"]), *message["data"])

        self.transport.write(rawmessage)

    def dataReceived(self, data):
        data = map(ord, data)
        message = dict(cdc=data[0], source=data[1], destination=data[2],
                       ack=data[3] & 0x80 > 0, ttl=(data[3] & 0x78) >> 3)
        message['data'] = []
        if data[4]:
            message['data'] = data[5:]
        self.client_message_received(message)


class TransportProtocol(protocol.Protocol):

    SEGMENT_FLAG_SEG = 0x4
    SEGMENT_FLAG_FIN = 0x2
    SEGMENT_FLAG_ACK = 0x1

    def __init__(self):
        self._inmsgbuffer = {}
        self._outmsgbuffer = {}

    def send_message(self, message):
        """ Converts Control Message to Segments and sends its """

        ack = ord(message[3]) & 0x80
        ttl = (ord(message[3]) & 0x78) >> 3
        assert ttl and ttl <= 15, "TTL should be between 1-15"

        if ack:
            self._outmsgbuffer[message] = dict(
                d=Deferred(), crcs=[],
                callid=reactor.callLater(ttl, self._messagelost_callback,
                                         message))

        for segment in self.message_to_segments(message):
            if ack:
                self._outmsgbuffer[message]["crcs"].append(segment[-2:])
            self.send_segment(segment)

        return (self._outmsgbuffer[message]["d"] if message in
                self._outmsgbuffer else True)

    def send_segment(self, segment):
        self.transport.write(segment)

    def message_received(self, message):
        pass

    def dataReceived(self, data):
        assert len(data) >= 6
        flags = ord(data[3]) >> 5

        # docs/specification/network/cdc/urg.html#cdc-urg-0x0a
        if ord(data[0]) == CHANNEL_URGENT.SEGMENT_ACKNOWLEDGMENT:
            return self._acknowledge_received(data)
        elif flags & self.SEGMENT_FLAG_ACK:
            self._send_acknowledge(data)

        # if message isn't segmented
        if not flags & self.SEGMENT_FLAG_SEG and flags & self.SEGMENT_FLAG_FIN:
            return self.message_received(self.segment_to_message(data))

        # else if segmented then need to wait for another segments
        key = data[0:3]
        order = ord(data[4])
        assert order <= 255

        if not key in self._inmsgbuffer:
            self._inmsgbuffer[key] = {}
        if not order in self._inmsgbuffer[key]:
            self._inmsgbuffer[key][order] = data[3:-2]

        message = self._inbufsegments_to_message(key)
        if message:
            self.message_received(message)

    @staticmethod
    def segment_to_message(segment):
        message = segment[0:3]
        message += pack("BB", (ord(segment[3]) & 0x20) << 2,
                        ord(segment[3]) & 0xF)
        message += segment[4:-2]
        return message

    @staticmethod
    def message_to_segments(message):
        segments = []
        cdc = message[0]
        sarp = message[1:3]
        flags = (TransportProtocol.SEGMENT_FLAG_ACK if ord(message[3]) & 0x80
                 else 0)
        data_len = (ord(message[3]) & 0x7) | ord(message[4])
        data = list(message[5:])
        segmented = data_len > 8

        if segmented:
            mdps = 7  # max data per segment
            flags |= TransportProtocol.SEGMENT_FLAG_SEG
        else:
            mdps = 8

        segorder = 0
        firstIter = True
        while data or firstIter:
            _data_part = data[:mdps]
            del data[0:mdps]
            firstIter = False

            if segmented:
                _data_part = [pack("B", segorder)] + _data_part
                segorder += 1

            if not data:
                flags |= TransportProtocol.SEGMENT_FLAG_FIN

            segment = cdc + sarp
            segment += pack("B", flags << 5 | len(_data_part))
            segment += "".join(_data_part)
            _crc = calc_crc16(map(ord, segment))
            segment += pack("BB", _crc >> 8, _crc & 0xFF)
            segments.append(segment)

        return segments

    def _send_acknowledge(self, segment):
        acksegment = pack("B", CHANNEL_URGENT.SEGMENT_ACKNOWLEDGMENT)
        acksegment += segment[2]
        acksegment += segment[1]
        acksegment += pack("B", self.SEGMENT_FLAG_FIN << 5 | 2)
        acksegment += segment[-2:]
        _crc = calc_crc16(map(ord, acksegment))
        acksegment += pack("BB", _crc >> 8, _crc & 0xFF)
        return self.send_segment(acksegment)

    def _acknowledge_received(self, segment):
        if not self._outmsgbuffer:
            return

        assert len(segment) == 8
        ackcrc = segment[4:6]

        for key, value in self._outmsgbuffer.items():
            if ackcrc in value["crcs"]:
                value["crcs"].remove(ackcrc)
                # if empty CRC list then all segments acknowledged
                if not value["crcs"]:
                    value["callid"].cancel()
                    value["d"].callback(True)
                    del self._outmsgbuffer[key]
                return

    def _messagelost_callback(self, message):
        if not message in self._outmsgbuffer:
            return
        self._outmsgbuffer[message]["d"].errback(Failure(
            SATPMessageLost("Message has been lost ")))
        del self._outmsgbuffer[message]

    def _inbufsegments_to_message(self, key):
        seg_nums = len(self._inmsgbuffer[key])
        max_index = max(self._inmsgbuffer[key].keys())
        last_segment = self._inmsgbuffer[key][max_index]
        seg_final = (ord(last_segment[0]) >> 5) & self.SEGMENT_FLAG_FIN

        if not seg_final or seg_nums != max_index+1:
            return None

        data_len = 0
        for s in self._inmsgbuffer[key].itervalues():
            data_len += len(s[2:])

        message = key
        message += pack("BB", data_len >> 8, data_len & 0xFF)
        for _order in range(seg_nums):
            message += self._inmsgbuffer[key][_order][2:]

        return message


class RoutingProtocol(protocol.Protocol):

    PACKET_SOP_CODE = "\x01"
    PACKET_HEADER_LEN = 4
    PACKET_MAXDATA_LEN = 8
    PACKET_CRC_LEN = 2
    PACKET_EOF_CODE = "\x17"

    BUFFER_IN_LEN = 16  # The sum of PACKET_* defines length

    def __init__(self):
        self._inbuffer = [0] * self.BUFFER_IN_LEN

    @staticmethod
    def segment_to_packet(segment):
        return (RoutingProtocol.PACKET_SOP_CODE + segment +
                RoutingProtocol.PACKET_EOF_CODE)

    @staticmethod
    def packet_to_segment(packet):
        return packet[1:-1]

    def packet_received(self, packet):
        pass

    def send_segment(self, segment):
        """ Converts Transport Segment to Routing Packet and sends it """

        return self.send_packet(RoutingProtocol.segment_to_packet(segment))

    def send_packet(self, packet):
        assert (packet[0] == self.PACKET_SOP_CODE and
                packet[-1] == self.PACKET_EOF_CODE)
        self.transport.write(packet)

    def dataReceived(self, data):
        for d in data:
            self._byte_received(d)

    def _byte_received(self, byte):
        self._buffer_push_byte(byte)

        if byte != self.PACKET_EOF_CODE:
            return

        start = self.BUFFER_IN_LEN - self.PACKET_CRC_LEN \
            - self.PACKET_HEADER_LEN - 2
        for i in reversed(range(0, start+1)):
            if self._inbuffer[i] != self.PACKET_SOP_CODE:
                continue

            if self._buffer_contains_packet(i):
                return self.packet_received(
                    "".join(self._inbuffer[i:]))

    def _buffer_push_byte(self, byte):
        del self._inbuffer[0]
        self._inbuffer.append(byte)

    def _buffer_contains_packet(self, sopindex):
        _data_len = ord(self._inbuffer[sopindex+self.PACKET_HEADER_LEN]) & 0xF

        if (_data_len > self.PACKET_MAXDATA_LEN or
            sopindex + self.PACKET_HEADER_LEN + _data_len +
            self.PACKET_CRC_LEN + 2 != self.BUFFER_IN_LEN):
            return False

        _crc = ord(self._inbuffer[self.BUFFER_IN_LEN-
                                  self.PACKET_CRC_LEN-1]) << 8
        _crc |= ord(self._inbuffer[self.BUFFER_IN_LEN-self.PACKET_CRC_LEN])

        _header_and_data = self._inbuffer[
            sopindex+1:
            sopindex+1+self.PACKET_HEADER_LEN+_data_len]
        return _crc == calc_crc16(map(ord, _header_and_data))


class TransportProtocolWrapping(TransportProtocol):

    def __init__(self, inmessage_callback):
        TransportProtocol.__init__(self)
        self.inmessage_callback = inmessage_callback

    def message_received(self, message):
        self.inmessage_callback(message)


class RoutingProtocolWrapping(RoutingProtocol):

    def __init__(self, inpacket_callback):
        RoutingProtocol.__init__(self)
        self.inpacket_callback = inpacket_callback

    def packet_received(self, packet):
        self.inpacket_callback(packet)


class ControlProtocolWrapping(ControlProtocol):

    def __init__(self, climessage_callback):
        self.climesage_callback = climessage_callback

    def client_message_received(self, message):
        self.climesage_callback(message)