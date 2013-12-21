.. |SA| replace:: SmartAnthill
.. |SACP| replace:: :ref:`SACP <sacp>`
.. |SATP| replace:: :ref:`SATP <satp>`
.. |SARP| replace:: :ref:`SARP <sarp>`
.. _OSI-Model: http://en.wikipedia.org/wiki/OSI_model
.. _CAN: http://en.wikipedia.org/wiki/CAN_bus
.. _RS-232: http://en.wikipedia.org/wiki/RS-232

.. _netmodel:

Network Model
=============

Comparasion with OSI Model
--------------------------

+--------+--------------+-------------+-----------+-----------+---------+
| Layers | OSI-Model_   | |SA| Model  | Protocol  | Data Unit | Service |
+========+==============+=============+===========+===========+=========+
| 7      | Application  | Application | |SACP|    | Message   | Queue   |
+--------+--------------+             +           +           +         +
| 6      | Presentation |             |           |           |         |
+--------+--------------+             +           +           +         +
| 5      | Session      |             |           |           |         |
+--------+--------------+-------------+-----------+-----------+---------+
| 4      | Transport    | Transport   | |SATP|    | Segment   | Queue   |
+--------+--------------+-------------+-----------+-----------+---------+
| 3      | Network      | Network     | |SARP|    | Packet    | Router  |
+--------+--------------+-------------+-----------+-----------+---------+
| 2      | Data-Link    | Data-Link   | CAN_      | Frame     | Bridge  |
+--------+--------------+-------------+-----------+-----------+---------+
| 1      | Physical     | Physical    | RS-232_   | Bit       |         |
+--------+--------------+-------------+-----------+-----------+---------+

