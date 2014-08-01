.. |SA| replace:: *SmartAnthill*

Installation
============

Python & OS Support
-------------------

|SA| is written in `Python <https://www.python.org>`_ and works with versions 2.6
and 2.7. |SA| works on Unix/Linux, OS X, and Windows.

All commands below should be executed in
`Command-line <http://en.wikipedia.org/wiki/Command-line_interface>`_
application in your *OS*:

* *Unix/Linux/OS X* this is *Terminal* application.
* *Windows* this is
  `Command Prompt <http://en.wikipedia.org/wiki/Command_Prompt>`_ (``cmd.exe``)
  application.

Super-Quick
-----------

To install or upgrade |SA|, download
`get-smartanthill.py <https://raw.githubusercontent.com/ivankravets/smartanthill/develop/get-smartanthill.py>`_ script.

Then run the following (which may require administrator access):

.. code-block:: bash

    $ python get-smartanthill.py

An alternative short version for *Mac/Linux* users:

.. code-block:: bash

    $ curl -L http://bit.ly/1qyr6K1 | python


On *Windows OS* it may look like:

.. code-block:: bash

    C:\Python27\python.exe get-smartanthill.py


Full Guide
----------

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
       <https://pip.pypa.io/en/latest/installing.html>`_.
    4. Add to *PATH* system variable ``;C:\Python27;C:\Python27\Scripts;`` and
       reopen *Command Prompt* (``cmd.exe``) application. Please read this
       article `How to set the path and environment variables in Windows
       <http://www.computerhope.com/issues/ch000549.htm>`_.


2. To install the latest release via
`PIP <https://pip.pypa.io/en/latest/index.html>`_:

.. code-block:: bash

    $ pip install smartanthill && pip install --egg scons

.. note::
    If your computer does not recognize ``pip`` command, try to install it
    first using
    `these instructions
    <https://pip.pypa.io/en/latest/installing.html>`_.

For upgrading the |SA| to new version please use this command:

.. code-block:: bash

    $ pip install -U smartanthill
