#!/usr/bin/env python
from setuptools import setup

setup(
    name='dscovered',
    version='0.0.1',
    url='http://github.com/peterfraedrich/discovered',
    license='MIT',
    author='Peter Fraedrich',
    author_email='peter.fraedrich@hexapp.net',
    description='Redis-based service discovery for python',
    packages=['discovered'],
    platforms='any',
    install_requires=[
        'redis',
        'psutil'
    ],
    keywords=[
        'Redis',
        'service discovery',
        'consensus',
        'discover'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
