.. |SA| replace:: SmartAnthill
.. |SANet| replace:: :ref:`sanet`

Welcome to SmartAnthill's Documentation
=======================================

:Release: |release|
:Status:  Planing
:Date:    |today|
:Author:  `Ivan Kravets <http://www.ikravets.com/about-me>`_


:ref:`sasys` is an intelligent micro-oriented networked system. It opens
the doors for people that not familiar with electronics and micro-controller
programming, but early had dream to use it. The main goal of |SA| is to
destroy the wall between usual user and hardware world. Thanks to this
system we can combine the independent micro-devices or micro-based networks
into general |SANet|.

You do not need to learn micro-programming languages, you do not need to install
any `IDE <http://en.wikipedia.org/wiki/Integrated_development_environment>`_
or `Toolchain <http://en.wikipedia.org/wiki/Toolchain>`_. All you need is to
connect micro-device to |SA|, to select capabilities that device should
have and *"train it"* [#]_ to behave as the network device.

Installation
------------

.. toctree::
    :maxdepth: 2

    installation/quickstart
    installation/configuration

Usage Documentation
-------------------

Developer Documentation
-----------------------

Specification
-------------

.. toctree::
    :maxdepth: 2

    specification/system/index
    specification/embedded/index
    specification/network/index


.. [#] The *"train it"* is that |SA| creates unique :ref:`saes` (firmware) for
    each supported micro-device and then installs it.
