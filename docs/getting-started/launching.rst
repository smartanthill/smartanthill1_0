.. |SA| replace:: *SmartAnthill*

Launching
=========

|SA| is based on `Twisted <http://en.wikipedia.org/wiki/Twisted_(software)>`_
and can be launched as *Foreground Process* as well as
`Background Process <http://en.wikipedia.org/wiki/Background_process>`_.

Foreground Process
------------------

The whole list of usage options for |SA| is accessible via:

.. code-block:: bash

    $ smartanthill --help

Quick launching (the current directory will be used as :ref:`wsdir`):

.. code-block:: bash

    $ smartanthill

Launching with specific :ref:`wsdir`:


.. code-block:: bash

    $  smartanthill --workspacedir=/path/to/workspace/directory


Check the :ref:`configuration` page for detailed configuration options.


Background Process
------------------

The launching in the *Background Process* implements through ``twistd`` utility.
The whole list of usage options for ``twistd`` is accessible via
``twistd --help`` command. The final |SA| command looks like:

.. code-block:: bash

    $ cd /path/to/workspace/directory
    $ twistd smartanthill



