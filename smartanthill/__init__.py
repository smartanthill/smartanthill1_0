# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

# pylint: disable=W1401

VERSION = (0, 0, 0)
FIRMWARE_VERSION = (1, 0)

__version__ = ".".join([str(s) for s in VERSION])

__title__ = "smartanthill"
__description__ = "An intelligent micro-oriented networking system"
__url__ = "http://smartanthill.ikravets.com"
__docsurl__ = "http://docs.smartanthill.ikravets.com"

__author__ = "Ivan Kravets"
__email__ = "me@ikravets.com"

__license__ = "MIT Licence"
__copyright__ = "Copyright (C) 2013-2014 Ivan Kravets"

__banner__ = """
      _________________________________________
     /                                        /\\     >< {description} ><
    /        \/             \\\\             __/ /\\    Home:    {home}
   /   ___  _@@    Smart    @@_  ___     /  \\/       Docs:    {docs}
  /   (___)(_)    Anthill    (_)(___)   /__          Issues:  {issues}
 /    //|| ||   {version:^11}   || ||\\\\     /\\         License: {license}
/_______________________________________/ /
\_______________________________________\/           Workspace: #wsdir#
 \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \\           Dashboard: #dashboard#
""".format(version=__version__,
           description=__description__,
           home=__url__,
           docs=__docsurl__,
           issues="https://github.com/ivankravets/smartanthill/issues",
           license=__copyright__ + ", " + __license__)
