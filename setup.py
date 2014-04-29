# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from setuptools import find_packages, setup

from smartanthill import (__author__, __description__, __email__, __license__,
                          __name__, __url__, __version__)

setup(
    name=__name__,
    version=__version__,
    description=__description__,
    long_description=open("README.rst").read(),
    author=__author__,
    author_email=__email__,
    url=__url__,
    license=__license__,
    install_requires=[
        "twisted>=11.1",
        "pyserial"
    ],
    packages=find_packages()+["twisted.plugins"],
    package_data={"smartanthill": ["*.json"]},
    entry_points={
        "console_scripts": [
            "smartanthill = smartanthill.__main__:main"
        ]
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Framework :: Twisted",
        "Intended Audience :: Customer Service",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: C",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        "Topic :: Adaptive Technologies",
        "Topic :: Communications",
        "Topic :: Home Automation",
        "Topic :: Internet",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol "
        "Translator",
        "Topic :: Software Development :: Compilers",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: System :: Distributed Computing",
        "Topic :: System :: Networking",
        "Topic :: Terminals :: Serial"
    ]
)
