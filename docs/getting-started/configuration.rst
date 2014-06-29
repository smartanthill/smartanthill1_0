.. |SA| replace:: *SmartAnthill*
.. |SASys| replace:: *SmartAnthill System*

.. _configuration:

Configuration
=============

|SA| uses `JSON <http://en.wikipedia.org/wiki/JSON>`_ human-readable format for
data serialization. This syntax is easy for using and reading.

The |SA| *Configuration Parser* gathers data in the next order (steps):

1. Loads predefined :ref:`baseconf` options.
2. Loads options from :ref:`wsdir`.
3. Loads :ref:`consoleopts`.

.. note::
    The *Configuration Parser* redefines options step by step (from #1 to #3).
    The :ref:`consoleopts` step has the highest priority.


.. _baseconf:

Base Configuration
------------------

The *Base Configuration* is predefined in |SASys|.
See `config_base.json <https://github.com/ivankravets/smartanthill/blob/develop/smartanthill/config_base.json>`_.


.. _wsdir:

Workspace Directory
-------------------

|SA| uses ``--workspacedir`` for:

* finding user's specific start-up configuration options. They must be located
  in the ``smartanthill.json`` file. (Check the list of the available options
  `here <https://github.com/ivankravets/smartanthill/blob/develop/smartanthill/config_base.json>`_)
* finding the *Addons* for |SASys|
* storing the settings about micro-devices
* storing the another working data.

For a start please **create empty directory** (like "project directory").
Later |SA| will fill this folder with proper data.

.. warning::
    The *Workspace Directory* must have `Written Permission
    <http://en.wikipedia.org/wiki/File_system_permissions>`_

.. _consoleopts:

Console Options
---------------

The simple options that are defined in :ref:`baseconf` can be redefined through
console options for |SA| *Application*.

The whole list of usage options for |SA| are accessible via:

.. code-block:: bash

    $ smartanthill --help

