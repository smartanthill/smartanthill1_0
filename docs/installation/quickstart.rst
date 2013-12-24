.. |SA| replace:: *SmartAnthill*
.. |SASys| replace:: *SmartAnthill System*

Quick-Start
===========

Requirements
------------

* Python >= 2.6, http://python.org
* Twisted >= 11.1, http://twistedmatrix.com/trac/
* PyYAML, http://pyyaml.org
* PySerial, http://pyserial.sourceforge.net

Installation
------------

.. warning::
    |SA| has not been released yet. Please
    `follow us <http://www.ikravets.com/smartanthill>`_ and you will be
    informed about all news.

To install the latest release via
`PIP <http://www.pip-installer.org/en/latest/index.html>`_:

.. code-block:: bash

    $ pip install smartanthill

To install the development version:

.. code-block:: bash

    $ git clone https://github.com/ivankravets/smartanthill.git
    $ cd smartanthill
    $ python setup.py install


.. _datadir:

Working Data Directory
----------------------

The only one option that is required for starting |SA| is ``--data`` (the path
to the working data directory, like "project directory"). |SA| will use this
folder for:

* finding user's specific start-up configuration options. They must be located
  in the ``config.yaml`` file. (Check the list of the available options at
  :ref:`configuration` page)
* finding the *Addons* for |SASys|
* storing the settings about micro-devices
* storing the another working data.

.. warning::
    The *Working Data Directory* must have `Written Permission
    <http://en.wikipedia.org/wiki/File_system_permissions>`_


Getting Started
---------------

|SA| is based on `Twisted <http://en.wikipedia.org/wiki/Twisted_(software)>`_
and can be started as
`Background Process <http://en.wikipedia.org/wiki/Background_process>`_ as well
as *Foreground Process*

Background Process
^^^^^^^^^^^^^^^^^^

The starting in the *Background Process* implements through ``twistd`` utility.
The whole list of usage options for ``twistd`` is accessible via ``twistd -h``
command. The final |SA| command looks like:

.. code-block:: bash

    $ twistd smartanthill --data=/path/to/working/data/directory

The whole list of usage options for |SA| is accessible via:

.. code-block:: bash

    $ twistd smartanthill --help

Foreground Process
^^^^^^^^^^^^^^^^^^

The command for *Foreground Process*:

.. code-block:: bash

    $ twistd --nodaemon smartanthill --data=/path/to/working/data/directory


Check the :ref:`configuration` page for detailed configuration options.
