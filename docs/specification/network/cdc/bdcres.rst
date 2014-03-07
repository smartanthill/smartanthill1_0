.. |SACP| replace:: :ref:`sacp`
.. |SATP| replace:: :ref:`satp`
.. |SARP| replace:: :ref:`sarp`
.. _ADC: http://en.wikipedia.org/wiki/Analog-to-   digital_converter
.. _MSB: http://en.wikipedia.org/wiki/Most_significant_bit
.. _LSB: http://en.wikipedia.org/wiki/Least_significant_bit

.. _cdc_bdcres:

Bi-Directional Communication (Response)
=======================================

.. _cdc_bdcres_0x09:

ListOperationalStates
---------------------

The result of request from :ref:`cdc_bdcreq` channel and :ref:`cdc_bdcreq_0x09`.
The *Payload* part will contain the list of activated *Operational States*.
Where each byte will be equal to :ref:`cdc` *ID*.

The *Message* by |SACP| will have the next structure:

+---------+--------------------+---------------+-------------------------------+
| Part    | Field name         | Length (bits) | Value                         |
+=========+====================+===============+===============================+
| Header  | Channel            | 2             | 0x03                          |
+         +--------------------+---------------+-------------------------------+
|         | Data Classifier    | 6             | 0x09                          |
+         +--------------------+---------------+-------------------------------+
|         | SARP               | 16            | |SARP| address information    |
+         +--------------------+---------------+-------------------------------+
|         | ACK                | 1             | Acknowledgment flag           |
+         +--------------------+---------------+-------------------------------+
|         | TTL                | 4             | Time to live                  |
+         +--------------------+---------------+-------------------------------+
|         | Data length        | 11            | 0x1                           |
+---------+--------------------+---------------+-------------------------------+
| Payload | Data               | 8             | The :ref:`cdc` *ID*           |
+---------+--------------------+---------------+-------------------------------+

.. note::
    If device has more then one activated *Operational State* then the
    *Payload* part of *Message* will have the next sequence of bytes ->
    ``cdcID1, cdcID2, ..., cdcIDN``


.. _cdc_bdcres_0x0A:

ConfigurePinMode
----------------

The result of request from :ref:`cdc_bdcreq` channel and :ref:`cdc_bdcreq_0x0A`.
The *Payload* part will contain the list of pins that was successfully
configured with specified mode.

The *Message* by |SACP| will have the next structure:

+---------+--------------------+---------------+-------------------------------+
| Part    | Field name         | Length (bits) | Value                         |
+=========+====================+===============+===============================+
| Header  | Channel            | 2             | 0x03                          |
+         +--------------------+---------------+-------------------------------+
|         | Data Classifier    | 6             | 0x0A                          |
+         +--------------------+---------------+-------------------------------+
|         | SARP               | 16            | |SARP| address information    |
+         +--------------------+---------------+-------------------------------+
|         | ACK                | 1             | Acknowledgment flag           |
+         +--------------------+---------------+-------------------------------+
|         | TTL                | 4             | Time to live                  |
+         +--------------------+---------------+-------------------------------+
|         | Data length        | 11            | 0x1                           |
+---------+--------------------+---------------+-------------------------------+
| Payload | Data               | 8             | The number of the pin         |
+---------+--------------------+---------------+-------------------------------+

.. note::
    If you specified more then one Pin using single *Message* then the
    *Payload* part of *Message* will have the next sequence of bytes ->
    ``pin1, pin2, ..., pinN``


.. _cdc_bdcres_0x0B:

ReadDigitalPin
--------------

The result of request from :ref:`cdc_bdcreq` channel and :ref:`cdc_bdcreq_0x0B`.
The *Payload* part will contain the result from requested pins. The result
value can be as ``0x1`` (high level) or ``0x0`` (low level).

The *Message* by |SACP| will have the next structure:

+---------+--------------------+---------------+-------------------------------+
| Part    | Field name         | Length (bits) | Value                         |
+=========+====================+===============+===============================+
| Header  | Channel            | 2             | 0x03                          |
+         +--------------------+---------------+-------------------------------+
|         | Data Classifier    | 6             | 0x0B                          |
+         +--------------------+---------------+-------------------------------+
|         | SARP               | 16            | |SARP| address information    |
+         +--------------------+---------------+-------------------------------+
|         | ACK                | 1             | Acknowledgment flag           |
+         +--------------------+---------------+-------------------------------+
|         | TTL                | 4             | Time to live                  |
+         +--------------------+---------------+-------------------------------+
|         | Data length        | 11            | 0x1                           |
+---------+--------------------+---------------+-------------------------------+
| Payload | Data               | 8             | The value (``0x1`` or         |
|         |                    |               | ``0x0``)                      |
+---------+--------------------+---------------+-------------------------------+

.. note::
    If you specified more then one Pin using single *Message* then the
    *Payload* part of *Message* will have the next sequence of bytes ->
    ``value1, value2, ..., valueN``


.. _cdc_bdcres_0x0C:

WriteDigitalPin
---------------

The result of request from :ref:`cdc_bdcreq` channel and :ref:`cdc_bdcreq_0x0C`.
The *Payload* part will contain the list of pins that was successfully
updated with specified values.

The *Message* by |SACP| will have the next structure:

+---------+--------------------+---------------+-------------------------------+
| Part    | Field name         | Length (bits) | Value                         |
+=========+====================+===============+===============================+
| Header  | Channel            | 2             | 0x03                          |
+         +--------------------+---------------+-------------------------------+
|         | Data Classifier    | 6             | 0x0C                          |
+         +--------------------+---------------+-------------------------------+
|         | SARP               | 16            | |SARP| address information    |
+         +--------------------+---------------+-------------------------------+
|         | ACK                | 1             | Acknowledgment flag           |
+         +--------------------+---------------+-------------------------------+
|         | TTL                | 4             | Time to live                  |
+         +--------------------+---------------+-------------------------------+
|         | Data length        | 11            | 0x1                           |
+---------+--------------------+---------------+-------------------------------+
| Payload | Data               | 8             | The number of the pin         |
+---------+--------------------+---------------+-------------------------------+

.. note::
    If you specified more then one Pin using single *Message* then the
    *Payload* part of *Message* will have the next sequence of bytes ->
    ``pin1, pin2, ..., pinN``


.. _cdc_bdcres_0x0D:

ConfigureAnalogReference
------------------------

The result of request from :ref:`cdc_bdcreq` channel and :ref:`cdc_bdcreq_0x0D`.
The first byte of *Payload* part will contain ``0x01`` if the reference
voltage was successfully configured, otherwise ``0x00``.

The *Message* by |SACP| will have the next structure:

+---------+--------------------+---------------+-------------------------------+
| Part    | Field name         | Length (bits) | Value                         |
+=========+====================+===============+===============================+
| Header  | Channel            | 2             | 0x03                          |
+         +--------------------+---------------+-------------------------------+
|         | Data Classifier    | 6             | 0x0A                          |
+         +--------------------+---------------+-------------------------------+
|         | SARP               | 16            | |SARP| address information    |
+         +--------------------+---------------+-------------------------------+
|         | ACK                | 1             | Acknowledgment flag           |
+         +--------------------+---------------+-------------------------------+
|         | TTL                | 4             | Time to live                  |
+         +--------------------+---------------+-------------------------------+
|         | Data length        | 11            | 0x1                           |
+---------+--------------------+---------------+-------------------------------+
| Payload | Data               | 8             | The result: ``0x00`` or       |
|         |                    |               | ``0x01``                      |
+---------+--------------------+---------------+-------------------------------+


.. _cdc_bdcres_0x0E:

ReadAnalogPin
-------------

The result of request from :ref:`cdc_bdcreq` channel and :ref:`cdc_bdcreq_0x0E`.
The *Payload* part will contain the result from requested pins. The result
value can be between 0-1023 (for 10-bit ADC_) or between 0-4095 (for
12-bit ADC_).

The *Message* by |SACP| will have the next structure:

+---------+--------------------+---------------+-------------------------------+
| Part    | Field name         | Length (bits) | Value                         |
+=========+====================+===============+===============================+
| Header  | Channel            | 2             | 0x03                          |
+         +--------------------+---------------+-------------------------------+
|         | Data Classifier    | 6             | 0x0E                          |
+         +--------------------+---------------+-------------------------------+
|         | SARP               | 16            | |SARP| address information    |
+         +--------------------+---------------+-------------------------------+
|         | ACK                | 1             | Acknowledgment flag           |
+         +--------------------+---------------+-------------------------------+
|         | TTL                | 4             | Time to live                  |
+         +--------------------+---------------+-------------------------------+
|         | Data length        | 11            | 0x2                           |
+---------+--------------------+---------------+-------------------------------+
| Payload | Data               | 8             | The MSB_ of result            |
+         +                    +---------------+-------------------------------+
|         |                    | 8             | The LSB_ of result            |
+---------+--------------------+---------------+-------------------------------+

.. note::
    If you specified more then one Pin using single *Message* then the
    *Payload* part of *Message* will have the next sequence of bytes ->
    ``MSB_value1, LSB_value1, MSB_value2, LSB_value2, ..., MSB_valueN,
    LSB_valueN``
