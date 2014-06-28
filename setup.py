#! /usr/bin/env python

from setuptools import setup

setup(
    name                 = 'filter-logins',
    version              = '0.0.1',
    author               = 'Brandon Forehand',
    author_email         = 'b4hand@users.sf.net',
    license              = 'MIT License',
    packages             = [],
    scripts              = ['filter_logins.py'],
    classifiers          = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers'
    ],
    install_requires     = [
        'python-dateutil==2.2',
        'flanker==0.3.14'
    ]
)
