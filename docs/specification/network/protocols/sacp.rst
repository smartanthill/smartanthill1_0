.. |NETMODEL| replace:: :ref:`netmodel`
.. |SACP| replace:: :ref:`sacp`
.. |SATP| replace:: :ref:`satp`
.. |SARP| replace:: :ref:`sarp`

.. _sacp:

Control Protocol (SACP)
=======================

|SACP| is a message based protocol with priority control. It resides at
the *Application Layer* of the |NETMODEL|. The priority logic underlies
the *Channel*. Each *Channel* has own *Data Classifier*.

Message structure
-----------------

+---------+--------------------+---------------+-------------------------------+
| Part    | Field name         | Length (bits) | Description                   |
+=========+====================+===============+===============================+
| Header  | Channel            | 2             | Channel ID (Priority)         |
+         +--------------------+---------------+-------------------------------+
|         | Data Classifier    | 6             | Data Classifier ID            |
+         +--------------------+---------------+-------------------------------+
|         | SARP               | 16            | SARP address information      |
+         +--------------------+---------------+-------------------------------+
|         | SATP               | 3             | SATP flags                    |
+         +--------------------+---------------+-------------------------------+
|         | Reserved           | 2             | Must be set to 0x0            |
+         +--------------------+---------------+-------------------------------+
|         | Data length        | 11            | Length of Data in bytes       |
+---------+--------------------+---------------+-------------------------------+
| Payload | Data               | 0-14336       | Maximum is 1792 bytes         |
+---------+--------------------+---------------+-------------------------------+

``Channel (2 bits)``
^^^^^^^^^^^^^^^^^^^^

This is a *Channel ID* that specifies the priority of this *Message*. The
smaller ID is, greater priority has the *Message*. For the whole channels
list please check the :ref:`cdc`.


``Data Classifier (6 bits)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Check the :ref:`cdc`.

``SARP (16 bits)``
^^^^^^^^^^^^^^^^^^

This is an address information that contains *Source and Destination IDs*
for |SARP|.

``SATP (3 bits)``
^^^^^^^^^^^^^^^^^

These are the *Segmentation*, *Final* and *Acknowledgment* flags for |SATP|.


``Data length (11 bits)``
^^^^^^^^^^^^^^^^^^^^^^^^^

This is a length of *Payload* part in bytes. The *Message* can be empty
(without *Payload*). In this situation when ``Data length=0x0`` *Payload* part
is not presented in the *Message*.

``Data (0-14336 bits)``
^^^^^^^^^^^^^^^^^^^^^^^
The maximum size of *Payload* part is 1792 bytes.

.. note::
    This limitation was caused by maximum numbers of *Segments* from |SATP|.
    ``256 segments * 7 bytes of user data = 1792 bytes``
