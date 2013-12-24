.. |SANET| replace:: *Network*
.. _CAN: http://en.wikipedia.org/wiki/CAN_bus
.. _Fieldbuses: http://en.wikipedia.org/wiki/Fieldbus

.. _sanet:

Network
=======

*SmartAnthill Network* is an independent micro-based and multi-master
network that allows devices to communicate with each other. The micro-based
device can be connected directly to |SANET| through the different routers (for
example,
`Serial Communication <http://en.wikipedia.org/wiki/Serial_communications>`_
over `Serial Port <http://en.wikipedia.org/wiki/Serial_port>`_).

The key feature of the |SANET| is communication with other networks. It can
be extended with another |SANET| or with Fieldbuses_, like CAN_.


.. toctree::
    :maxdepth: 2

    netmodel
    protocols/index
    can
    zvd
