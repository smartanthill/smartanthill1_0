.. |SA| replace:: *SmartAnthill*
.. |SASys| replace:: *SmartAnthill System*

.. _configuration:

Configuration
=============

|SA| uses `JSON <http://en.wikipedia.org/wiki/JSON>`_ human-readable format for
data serialization. This syntax is easy for using and reading.

The |SA| *Configuration Parser* gathers data in the next order (steps):

1. Loads predefined :ref:`baseconf` options.
2. Loads :ref:`workingconf` options from :ref:`datadir`.
3. Loads :ref:`consoleopts`.

.. note::
    The *Configuration Parser* redefines options step by step (from #1 to #3).
    The :ref:`consoleopts` step has the highest priority.


.. _baseconf:

Base Configuration
------------------
The *Base Configuration* is predefined in |SASys|:

.. literalinclude:: ../../smartanthill/config_base.json
   :language: json


.. _workingconf:

Working Configuration
---------------------

.. _consoleopts:

Console Options
---------------

The simple options that are defined in :ref:`baseconf` can be redefined through
console options for |SA| *Application*.

The whole list of usage options for |SA| are accessible via:

.. code-block:: bash

    $ twistd smartanthill --help

