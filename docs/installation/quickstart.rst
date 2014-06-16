.. |SA| replace:: *SmartAnthill*
.. |SASys| replace:: *SmartAnthill System*

Quick-Start
===========

Python & OS Support
-------------------

|SA| is written in `Python <https://www.python.org>`_ and works with versions 2.6
and 2.7.

|SA| works on Unix/Linux, OS X, and Windows.


Installation
------------

All commands below should be executed in
`Command-line <http://en.wikipedia.org/wiki/Command-line_interface>`_
application in your OS:

* *Unix/Linux/OS X* this is *Terminal* application.
* *Windows* this is
  `Command Prompt <http://en.wikipedia.org/wiki/Command_Prompt>`_ (``cmd.exe``)
  application.

1. Check ``python`` version:

.. code-block:: bash

    $ python --version

.. note::
    *Windows OS Users* only:

    1. `Download Python <https://www.python.org/downloads/>`_ and install it.
    2. Download and install
       `Python for Windows extensions
       <http://sourceforge.net/projects/pywin32/files/pywin32/Build%20218/>`_.
    3. Install *Python Package Index* utility using
       `these instructions
       <http://www.pip-installer.org/en/latest/installing.html>`_.
    4. Add to *PATH* system variable ``;C:\Python27;C:\Python27\Scripts;`` and
       reopen *Command Prompt* (``cmd.exe``) application. Please read this
       article `How to set the path and environment variables in Windows
       <http://www.computerhope.com/issues/ch000549.htm>`_.


2. To install the latest release via
`PIP <http://www.pip-installer.org/en/latest/index.html>`_:

.. code-block:: bash

    $ pip install smartanthill

.. note::
    If your computer does not recognize ``pip`` command, try to install it
    first using
    `these instructions
    <http://www.pip-installer.org/en/latest/installing.html>`_.

To install the development version:

.. code-block:: bash

    $ git clone https://github.com/ivankravets/smartanthill.git
    $ cd smartanthill
    $ python setup.py install


.. _datadir:

Working Data Directory
----------------------

The only one requirement for starting |SA| is creation of
*Working Data Directory*. |SA| will use this directory for:

* finding user's specific start-up configuration options. They must be located
  in the ``config.json`` file. (Check the list of the available options at
  :ref:`configuration` page)
* finding the *Addons* for |SASys|
* storing the settings about micro-devices
* storing the another working data.

For a start please **create empty directory** (like "project directory").
Later |SA| will fill this folder with proper data.

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

    $ cd /path/to/working/data/directory
    $ twistd smartanthill

The whole list of usage options for |SA| is accessible via:

.. code-block:: bash

    $ twistd smartanthill --help

Foreground Process
^^^^^^^^^^^^^^^^^^

The command for *Foreground Process*:

.. code-block:: bash

    $ cd /path/to/working/data/directory
    $ twistd --nodaemon smartanthill


Check the :ref:`configuration` page for detailed configuration options.
