# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

# pylint: disable=W1401

VERSION = (0, 0, 0)
__version__ = ".".join([str(s) for s in VERSION])
__banner__ = """
      _________________________________________
     /                                        /\\     >< {title} ><
    /        \/             \\\\             __/ /\\    Home:    {home}
   /   ___  _@@    Smart    @@_  ___     /  \\/       Docs:    {docs}
  /   (___)(_)    Anthill    (_)(___)   /__          Issues:  {issues}
 /    //|| ||   {version:^11}   || ||\\\\     /\\         License: {license}
/_______________________________________/ /
\_______________________________________\/           Launched with data: #data#
 \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \\           Portal: #portal#
""".format(version=__version__,
           title="An intelligent micro-oriented networking system",
           home="http://www.ikravets.com/smartanthill",
           docs="http://smartanthill.readthedocs.org/en/latest/index.html",
           issues="https://github.com/ivankravets/smartanthill/issues",
           license="Copyright (c) Ivan Kravets, MIT Licence")
