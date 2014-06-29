.. |SA| replace:: *SmartAnthill*
.. |SANet| replace:: *SmartAnthill Network*

Welcome to SmartAnthill's Documentation
=======================================

:Release: |release|
:Date:    |today|
:Author:  `Ivan Kravets <http://www.ikravets.com/about-me>`_
:Home:    http://smartanthill.ikravets.com

.. warning::
    |SA| has not been released yet. The documentation is being updated. Please
    `follow us <http://smartanthill.ikravets.com>`_ and you will be
    informed about all news.

**SmartAnthill System** is an intelligent micro-oriented networking system.
It opens the door for people that are not familiar with electronics and
micro-controller programming, but earlier had dream to use it. The main goal of
|SA| is to destroy the wall between usual user and hardware world. Thanks to
this system we can combine the independent micro-devices or micro-based
networks into general |SANet|.

You do not need to learn micro-programming languages, you do not need to install
any `IDE <http://en.wikipedia.org/wiki/Integrated_development_environment>`_
or `Toolchain <http://en.wikipedia.org/wiki/Toolchain>`_. All you need is to
connect micro-device to |SA|, to select capabilities that device should
have and *"train it"* [#]_ to behave as the network device.

Getting Started
---------------

.. toctree::
    :maxdepth: 2

    getting-started/installation
    getting-started/launching
    getting-started/configuration

Usage Documentation
-------------------

Developer Documentation
-----------------------

Specification
-------------

.. toctree::
    :maxdepth: 2

    specification/network/index
    specification/system/index
    specification/embedded/index


.. [#] The *"train it"* is that |SA| creates unique :ref:`esystem`
    (firmware) for each supported micro-device and then installs it.
