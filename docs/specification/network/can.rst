.. |SA| replace:: SmartAnthill
.. |SANet| replace:: :ref:`sanet`
.. |SACP| replace:: :ref:`sacp`
.. |SATP| replace:: :ref:`satp`
.. |SARP| replace:: :ref:`SARP<sarp>`
.. _CAN: http://en.wikipedia.org/wiki/CAN_bus

.. _intcan:

Integration with CAN
====================
`CAN bus <http://en.wikipedia.org/wiki/CAN_bus>`_ is a message-based protocol,
designed specifically for automotive applications but now also used in other
areas such as aerospace, maritime, industrial automation and medical equipment
(got from `wiki <http://en.wikipedia.org/wiki/CAN_bus>`_).

Protocol
--------

|SANet| can be easy integrated with ``CAN`` because the
protocols of these networks are frame-based. ``CAN`` resides on the
*Data-Link Layer* of the |SANet| Model and represented with data unit as
*Frame*. While the *Network Layer* operates through :ref:`sarp` and
*Packet*. Therefore, |SARP| will work over ``CAN Protocol 2.0B``
(specification with extended message formats).

The *Data Length* field of the *Packet* from |SARP| is equivalent with ``CAN``
*Frame*. The |SARP| *Header* part can be converted to ``CAN`` *Extended
Identifier (29 bit)*.

Frame structure
^^^^^^^^^^^^^^^

+---------+--------------------+----+----------+-------------------------------+
| Part    | Field name         | Length (bits) | Description                   |
+=========+====================+====+==========+===============================+
| Header  | SACP               | 29 | 10       | SACP Data Classifier          |
+         +--------------------+    +----------+-------------------------------+
|         | SARP               |    | 16       | SARP address information      |
+         +--------------------+    +----------+-------------------------------+
|         | SATP               |    | 3        | SATP flags                    |
+---------+--------------------+----+----------+-------------------------------+
| Length  | Data length        | 4             | The length of data in bytes   |
+---------+--------------------+----+----------+-------------------------------+
| Payload | Data               | 0-64          | Max 8 bytes                   |
+---------+--------------------+----+----------+-------------------------------+

.. note::
    The fields `Start of Frame`, `Cyclic redundancy check` and `End of Frame`
    are not presented in this structure because the CAN_ protocol has own
    implementation for its.

``SACP (10 bits)``
******************
The *Channel* and *Data Classifier* for |SACP|.

``SARP (16 bits)``
******************
The address information that contains *Source and Destination IDs* for
:ref:`sarp`.

``SATP (3 bits)``
*****************
The *Segmentation*, *Final* and *Acknowledgment* flags for |SATP|

``Data length (4 bits)``
************************
The length of *Payload* part in bytes. The *Frame* can be empty (without
*Payload*). In this situation ``Data length=0x0`` and *Payload* is not
presented in the *Frame*. The maximum size of *Payload* part is 8 bytes.

``Data (0-64 bits)``
********************
The *Payload* data for |SATP|.
