.. |SACP| replace:: :ref:`sacp`
.. |SATP| replace:: :ref:`satp`
.. |SARP| replace:: :ref:`sarp`

.. _cdc_urg:

Urgent
======

The channel with the highest priority. It uses for the critical
tasks or operations.


.. _cdc_urg_0x0A:

Segment Acknowledgment
----------------------

Uses for acknowledge that *Segment* from sender was received and verified.
The *Segment* by |SATP| should have the next structure:

+---------+--------------------+---------------+-------------------------------+
| Part    | Field name         | Length (bits) | Value                         |
+=========+====================+===============+===============================+
| Header  | Channel            | 2             | 0x00                          |
+         +--------------------+---------------+-------------------------------+
|         | Data Classifier    | 6             | 0x0A                          |
+         +--------------------+---------------+-------------------------------+
|         | SARP               | 16            | |SARP| address information    |
+         +--------------------+---------------+-------------------------------+
|         | SEG                | 1             | 0x0                           |
+         +--------------------+---------------+-------------------------------+
|         | FIN                | 1             | 0x1                           |
+         +--------------------+---------------+-------------------------------+
|         | ACK                | 1             | 0x0                           |
+         +--------------------+---------------+-------------------------------+
|         | Reserved           | 1             | Must be set to 0x0            |
+         +--------------------+---------------+-------------------------------+
|         | Data length        | 4             | 0x2                           |
+---------+--------------------+---------------+-------------------------------+
| Payload | Data               | 16            | The *CRC* field from          |
|         |                    |               | received *Packet*             |
+---------+--------------------+---------------+-------------------------------+
