.. |NETMODEL| replace:: :ref:`netmodel`
.. |SA| replace:: SmartAnthill
.. |SACP| replace:: :ref:`sacp`
.. |SATP| replace:: :ref:`satp`
.. |SARP| replace:: :ref:`sarp`
.. |SANet| replace:: :ref:`sanet`

.. _sarp:

Routing Protocol (SARP)
=======================

The main goal of the |SARP| is to find a route and transfer a packet to
destination device that located in the |SANet|. The |SARP| does not guarantee
delivery. The only thing that it guarantees is integrity of the *Header* and
the *Payload* data in the packet (based on CRC).

Packet structure
----------------

+---------+--------------------+---------------+-------------------------------+
| Part    | Field name         | Length (bits) | Description                   |
+=========+====================+===============+===============================+
|         | SOP                | 8             | Start of packet               |
+---------+--------------------+---------------+-------------------------------+
| Header  | SACP               | 8             | SACP Data Classifier          |
+         +--------------------+---------------+-------------------------------+
|         | Source device      | 8             | The source device ID          |
+         +--------------------+---------------+-------------------------------+
|         | Destination device | 8             | The destination device ID     |
+         +--------------------+---------------+-------------------------------+
|         | SATP               | 3             | SATP flags                    |
+         +--------------------+---------------+-------------------------------+
|         | Reserved           | 1             | Must be set to 0x0            |
+         +--------------------+---------------+-------------------------------+
|         | Data length        | 4             | The length of data in bytes   |
+---------+--------------------+---------------+-------------------------------+
| Payload | Data               | 0-64          | Max 8 bytes                   |
+---------+--------------------+---------------+-------------------------------+
|         | CRC                | 16            | Checksum                      |
+---------+--------------------+---------------+-------------------------------+
|         | EOF                | 8             | End of packet                 |
+---------+--------------------+---------------+-------------------------------+

``SOP (8 bits)``
^^^^^^^^^^^^^^^^

It specifies the start of the packet. These 8 bits are equal to `ASCII Start Of
Heading (SOH) <http://en.wikipedia.org/wiki/C0_and_C1_control_codes>`_
character ``0x1``.

``SACP (8 bits)``
^^^^^^^^^^^^^^^^^^

These are the *Channel* and *Data Classifier* for |SACP|.

``Source device (8 bits)``
^^^^^^^^^^^^^^^^^^^^^^^^^^

This is an *Identifier (ID)* of the source device. |SANet| supports up to 255
devices. Each device has unique identifier from range 0-255. The device with
``ID=0x0`` corresponds to :ref:`zvd`.

``Destination device (8 bits)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is an *Identifier (ID)* of destination device. |SANet| supports up to 255
devices. Each device has unique identifier from range 0-255. The device with
``ID=0x0`` corresponds to :ref:`zvd`.

``SATP (3 bits)``
^^^^^^^^^^^^^^^^^

These are the *Segmentation*, *Final* and *Acknowledgment* flags for |SATP|.

``Data length (4 bits)``
^^^^^^^^^^^^^^^^^^^^^^^^

This is a length of *Payload* data in bytes. The *Packet* can be empty (without
*Payload*). In this situation ``Data length=0x0`` and *Payload* part is not
present in the *Packet*. The maximum size of *Payload* part are 8 bytes.

``Data (0-64 bits)``
^^^^^^^^^^^^^^^^^^^^

This is a *Payload* part for |SATP|.

``CRC (16 bits)``
^^^^^^^^^^^^^^^^^

The 16-bit checksum is used for error-checking of the *Header* and *Payload*
parts.

``EOF (8 bits)``
^^^^^^^^^^^^^^^^

It specifies the end of the packet. These 8 bits are equal to `ASCII End of
Transmission (SOH) <http://en.wikipedia.org/wiki/C0_and_C1_control_codes>`_
character ``0x17``.
