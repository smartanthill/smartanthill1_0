.. |SACP| replace:: :ref:`sacp`
.. |SATP| replace:: :ref:`satp`
.. |SARP| replace:: :ref:`sarp`

.. _cdc_bdcreq:

Bi-Directional Communication (Request)
======================================

.. _cdc_bdcreq_0x09:

ListOperationalStates
---------------------

Retrieve a list with activated *Operational States* for specified device.
For the result please read :ref:`cdc_bdcres_0x09` from :ref:`cdc_bdcres` channel.

The *Message* by |SACP| should have the next structure:

+---------+--------------------+---------------+-------------------------------+
| Part    | Field name         | Length (bits) | Value                         |
+=========+====================+===============+===============================+
| Header  | Channel            | 2             | 0x02                          |
+         +--------------------+---------------+-------------------------------+
|         | Data Classifier    | 6             | 0x09                          |
+         +--------------------+---------------+-------------------------------+
|         | SARP               | 16            | |SARP| address information    |
+         +--------------------+---------------+-------------------------------+
|         | ACK                | 1             | Acknowledgment flag           |
+         +--------------------+---------------+-------------------------------+
|         | TTL                | 4             | Time to live                  |
+         +--------------------+---------------+-------------------------------+
|         | Data length        | 11            | 0x0                           |
+---------+--------------------+---------------+-------------------------------+
| Payload | Data               | 0             | Without *Payload* part        |
+---------+--------------------+---------------+-------------------------------+


.. _cdc_bdcreq_0x0A:

ConfigurePinMode
----------------

Configure the specified pin to behave either as an:

* ``INPUT``
* ``OUTPUT``
* ``INPUT_PULLUP``
* ``INPUT_PULLDOWN``

For the result please read :ref:`cdc_bdcres_0x0A` from :ref:`cdc_bdcres` channel.

The *Message* by |SACP| should have the next structure:

+---------+--------------------+---------------+-------------------------------+
| Part    | Field name         | Length (bits) | Value                         |
+=========+====================+===============+===============================+
| Header  | Channel            | 2             | 0x02                          |
+         +--------------------+---------------+-------------------------------+
|         | Data Classifier    | 6             | 0x0A                          |
+         +--------------------+---------------+-------------------------------+
|         | SARP               | 16            | |SARP| address information    |
+         +--------------------+---------------+-------------------------------+
|         | ACK                | 1             | Acknowledgment flag           |
+         +--------------------+---------------+-------------------------------+
|         | TTL                | 4             | Time to live                  |
+         +--------------------+---------------+-------------------------------+
|         | Data length        | 11            | 0x2                           |
+---------+--------------------+---------------+-------------------------------+
| Payload | Data               | 8             | The number of the pin         |
+         +                    +---------------+-------------------------------+
|         |                    | 8             | The mode of the pin           |
|         |                    |               | (see table above)             |
+---------+--------------------+---------------+-------------------------------+

.. note::
    You can configure more than one Pin using single *Message*. Please use the
    next sequence of bytes in *Payload* part of *Message* -> ``pin1, mode1,
    pin2, mode2, ..., pinN, modeN``


.. _cdc_bdcreq_0x0B:

ReadDigitalPin
--------------

Read the value from a specified digital pin. For the result please read
:ref:`cdc_bdcres_0x0B` from :ref:`cdc_bdcres` channel.

The *Message* by |SACP| should have the next structure:

+---------+--------------------+---------------+-------------------------------+
| Part    | Field name         | Length (bits) | Value                         |
+=========+====================+===============+===============================+
| Header  | Channel            | 2             | 0x02                          |
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
| Payload | Data               | 8             | The number of the pin         |
+---------+--------------------+---------------+-------------------------------+

.. note::
    You can read more than one Pin using single *Message*. Please use the next
    sequence of bytes in *Payload* part of *Message* -> ``pin1, pin2, ...,
    pinN``


.. _cdc_bdcreq_0x0C:

WriteDigitalPin
---------------

Write a ``LOW`` or a ``HIGH`` level to a digital pin.
For the result please read :ref:`cdc_bdcres_0x0C` from :ref:`cdc_bdcres` channel.

The *Message* by |SACP| should have the next structure:

+---------+--------------------+---------------+-------------------------------+
| Part    | Field name         | Length (bits) | Value                         |
+=========+====================+===============+===============================+
| Header  | Channel            | 2             | 0x02                          |
+         +--------------------+---------------+-------------------------------+
|         | Data Classifier    | 6             | 0x0C                          |
+         +--------------------+---------------+-------------------------------+
|         | SARP               | 16            | |SARP| address information    |
+         +--------------------+---------------+-------------------------------+
|         | ACK                | 1             | Acknowledgment flag           |
+         +--------------------+---------------+-------------------------------+
|         | TTL                | 4             | Time to live                  |
+         +--------------------+---------------+-------------------------------+
|         | Data length        | 11            | 0x2                           |
+---------+--------------------+---------------+-------------------------------+
| Payload | Data               | 8             | The number of the pin         |
+         +                    +---------------+-------------------------------+
|         |                    | 8             | The level (``0x1=HIGH`` or    |
|         |                    |               | ``0x0=LOW``)                  |
+---------+--------------------+---------------+-------------------------------+

.. note::
    You can write to more than one Pin using single *Message*. Please use the
    next sequence of bytes in *Payload* part of *Message* -> ``pin1, value1,
    pin2, value2, ..., pinN, valueN``


.. _cdc_bdcreq_0x0D:

ConfigureAnalogReference
------------------------

Configure the reference voltage used for analog input. The modes are:

* ``DEFAULT``
* ``INTERNAL``
* ``INTERNAL1V1``
* ``INTERNAL2V56``
* ``INTERNAL1V5``
* ``INTERNAL2V5``
* ``EXTERNAL``

For the result please read :ref:`cdc_bdcres_0x0D` from :ref:`cdc_bdcres` channel.

The *Message* by |SACP| should have the next structure:

+---------+--------------------+---------------+-------------------------------+
| Part    | Field name         | Length (bits) | Value                         |
+=========+====================+===============+===============================+
| Header  | Channel            | 2             | 0x02                          |
+         +--------------------+---------------+-------------------------------+
|         | Data Classifier    | 6             | 0x0D                          |
+         +--------------------+---------------+-------------------------------+
|         | SARP               | 16            | |SARP| address information    |
+         +--------------------+---------------+-------------------------------+
|         | ACK                | 1             | Acknowledgment flag           |
+         +--------------------+---------------+-------------------------------+
|         | TTL                | 4             | Time to live                  |
+         +--------------------+---------------+-------------------------------+
|         | Data length        | 11            | 0x1                           |
+---------+--------------------+---------------+-------------------------------+
| Payload | Data               | 8             | The mode (see table above)    |
+---------+--------------------+---------------+-------------------------------+


.. _cdc_bdcreq_0x0E:

ReadAnalogPin
-------------

Read the value from a specified analog pin. For the result please read
:ref:`cdc_bdcres_0x0E` from :ref:`cdc_bdcres` channel.

The *Message* by |SACP| should have the next structure:

+---------+--------------------+---------------+-------------------------------+
| Part    | Field name         | Length (bits) | Value                         |
+=========+====================+===============+===============================+
| Header  | Channel            | 2             | 0x02                          |
+         +--------------------+---------------+-------------------------------+
|         | Data Classifier    | 6             | 0x0E                          |
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
    You can read more than one Pin using single *Message*. Please use the next
    sequence of bytes in *Payload* part of *Message* -> ``pin1, pin2, ...,
    pinN``
