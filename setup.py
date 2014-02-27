from setuptools import find_packages, setup

from smartanthill import __version__

setup(
    name='smartanthill',
    version=__version__,
    description='An intelligent micro-oriented networking system',
    long_description=open("README.rst").read(),
    author='Ivan Kravets',
    author_email='me@ikravets.com',
    url='http://www.ikravets.com/smartanthill',
    license='MIT Licence',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Twisted',
        'Intended Audience :: Customer Service',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Manufacturing',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: C',
        'Programming Language :: JavaScript',
        'Programming Language :: Python',
        'Topic :: Adaptive Technologies',
        'Topic :: Communications',
        'Topic :: Home Automation',
        'Topic :: Internet',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Software Development :: Compilers',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: System :: Distributed Computing',
        'Topic :: System :: Networking',
        'Topic :: Terminals :: Serial'
    ],
    install_requires=map(lambda l: l.strip(),
                         open("requirements.txt").readlines()),
    packages=find_packages()+['twisted.plugins'],
    package_data={
        '': ['*.json'],
        'twisted': ['plugins/smartanthill_plugin.py']
    },
    include_package_data=True
)
