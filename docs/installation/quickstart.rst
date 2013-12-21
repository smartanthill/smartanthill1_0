.. |SA| replace:: *SmartAnthill*

Quick-Start
===========

Requirements
------------

* Python >= 2.6, http://python.org
* Twisted >= 11.1, http://twistedmatrix.com/trac/
* PyYAML, http://pyyaml.org
* PySerial, http://pyserial.sourceforge.net

Download
--------

Using `PIP <http://www.pip-installer.org/en/latest/index.html>`_::

    pip install smartanthill

Go to https://github.com/ivankravets/smartanthill if you need to download
a package or clone the repository.


.. _datadir:

Working Data Directory
----------------------

The only one option that is required for starting |SA| is ``--data`` (the path
to working data directory, like "project directory"). |SA| will use this
folder for:

* to find user's specific start-up configuration options. They must be located
  in the ``config.yaml`` file. (Check the list of the available options at
  :ref:`configuration` page)
* to find the *Addons* for :ref:`sasys`
* to store the settings about micro-devices
* to store the another working data.

.. warning::
    The *Working Data Directory* must have `Write Permission
    <http://en.wikipedia.org/wiki/File_system_permissions>`_


Launch
------

|SA| is based on `Twisted <http://en.wikipedia.org/wiki/Twisted_(software)>`_
and can be launched as
`Background Process <http://en.wikipedia.org/wiki/Background_process>`_ well as
*Foreground Process*

Background Process
^^^^^^^^^^^^^^^^^^
The launching in *Background Process* implements through ``twistd`` utility. The
whole list of usage options for ``twistd`` are accessible via ``twistd -h``
command. The final |SA| command looks like::

    twistd smartanthill --data=/path/to/working/data/directory

The whole list of usage options for |SA| are accessible via::

    twistd smartanthill --help

Foreground Process
^^^^^^^^^^^^^^^^^^
The command for *Foreground Process*::

    twistd --nodaemon smartanthill --data=/path/to/working/data/directory


Check the :ref:`configuration` page for detail configuration options.
