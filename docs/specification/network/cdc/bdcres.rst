.. |SACP| replace:: :ref:`sacp`
.. |SATP| replace:: :ref:`satp`
.. |SARP| replace:: :ref:`sarp`

.. _cdc_bdcres:

Bi-Directional Communication (Response)
=======================================

.. _cdc_bdcres_0x0B:

ReadDigitalPin
--------------

The result of request from :ref:`cdc_bdcreq` channel and :ref:`cdc_bdcreq_0x0B`.
The returned value can be as ``0x1`` (high level) or ``0x0`` (low level).

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
|         | SATP               | 3             | |SATP| flags                  |
+         +--------------------+---------------+-------------------------------+
|         | Reserved           | 2             | Must be set to 0x0            |
+         +--------------------+---------------+-------------------------------+
|         | Data length        | 11            | 0x2                           |
+---------+--------------------+---------------+-------------------------------+
| Payload | Data               | 8             | The number of the pin         |
+         +                    +---------------+-------------------------------+
|         |                    | 8             | The value (``0x1`` or         |
|         |                    |               | ``0x0``)                      |
+---------+--------------------+---------------+-------------------------------+

.. note::
    If you specified more then one Pin using single *Message* then the *Data*
    part of *Message* will have the next sequence of bytes ->``pin1, value1,
    pin2, value2, ..., pinN, valueN``
