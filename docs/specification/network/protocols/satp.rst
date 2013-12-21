.. |NETMODEL| replace:: :ref:`netmodel`
.. |SACP| replace:: :ref:`sacp`
.. |SATP| replace:: :ref:`satp`
.. |SARP| replace:: :ref:`sarp`

.. _satp:

Transport Protocol (SATP)
=========================

|SATP| resides between |SACP| and |SARP| and operates with the two data units
(*Message* and *Segment*). Therefore, he has bi-directional work.

Between *Application Layer* and *Transport Layer* of the |NETMODEL|, it
divide into *Segments* the outbound *Message*. While between *Transport Layer*
and *Network Layer* it assembles multiple inbound *Segments* into single
*Message*.

|SATP| is the reliable protocol. It can guarantee delivery of each *Segment* if
source device asked it. Also it can guarantee the integrity of final *Message*
because |SATP| knows about order of each *Segment*.

Segment structure
-----------------

+---------+--------------------+---------------+-------------------------------+
| Part    | Field name         | Length (bits) | Description                   |
+=========+====================+===============+===============================+
| Header  | SACP               | 10            | SACP Data Classifier          |
+         +--------------------+---------------+-------------------------------+
|         | SARP               | 16            | SARP address information      |
+         +--------------------+---------------+-------------------------------+
|         | SEG                | 1             | Segmentation flag             |
+         +--------------------+---------------+-------------------------------+
|         | FIN                | 1             | Final segment flag            |
+         +--------------------+---------------+-------------------------------+
|         | ACK                | 1             | Acknowledgment flag           |
+         +--------------------+---------------+-------------------------------+
|         | Data length        | 4             | Length of Data in bytes       |
+---------+--------------------+---------------+-------------------------------+
| Payload | Data               | 0-64          | Maximum is 8 bytes            |
+---------+--------------------+---------------+-------------------------------+


``SACP (10 bits)``
^^^^^^^^^^^^^^^^^^

The *Channel* and *Data Classifier* for |SACP|.

``SARP (16 bits)``
^^^^^^^^^^^^^^^^^^

The address information that contains *Source and Destination IDs* for |SARP|.

``SEG (1 bit)``
^^^^^^^^^^^^^^^

The *Segmentation* flag. If the *Message* is not segmented then ``SEG=0``
otherwise ``SEG=1``.

.. note::
    The service information about *Segments Order* is located in the first byte
    of *Data* field. Hence it follows that the maximum number of *Segments* is
    256. The first *Segment* marks as ``0x0``, the second as ``0x1``
    and the last as ``0xFF``

``FIN (1 bit)``
^^^^^^^^^^^^^^^

Indicates that this *Segment* is final.

``ACK (1 bit)``
^^^^^^^^^^^^^^^

This is *Acknowledgment* flag. If ``ACK=1`` then this *Message* should be
confirmed by recipient about reception.

``Data length (4 bits)``
^^^^^^^^^^^^^^^^^^^^^^^^

The length of *Payload* part in bytes. The *Segment* can be empty (without
*Payload*). In this situation when ``Data length=0x0``, ``SEG=0`` and ``FIN=1``
*Payload* part is not presented in the *Segment*. The maximum size of *Payload*
part is 8 bytes.

``Data (0-64 bits)``
^^^^^^^^^^^^^^^^^^^^

The *Payload* data. If ``SEG=1`` the first byte of the data will be used for
*Segments Order* information and another 7 are available for user.
