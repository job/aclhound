#!/usr/bin/env python
# Copyright (C) 2014 Job Snijders <job@instituut.net>
#
# This file is part of ACLHound
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF TH

version = "0.8"

import codecs
import os
import sys

from setuptools import setup, find_packages, Extension
from os.path import abspath, dirname, join

here = abspath(dirname(__file__))

# determine the python version
IS_PYPY = hasattr(sys, 'pypy_version_info')

with codecs.open(join(here, 'README.rst'), encoding='utf-8') as f:
    README = f.read()

if sys.argv[-1] == 'publish':
    os.system('python2.7 setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

setup(
    name='aclhound',
    version=version
    maintainer="Job Snijders",
    maintainer_email='job@instituut.net',
    url='https://github.com/job/aclhound',
    description='ACL Compiler',
    long_description=README,
    license='BSD 2-Clause',
    keywords='acl python ciscoasa ciscoios routing networking',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    setup_requires=['nose', 'coverage'],
    packages=find_packages(exclude=['tests', 'tests.*']),
    test_suite='nose.collector',
    entry_points={'console_scripts': ['aclhound = aclhound.cli:main']},
    **extra_kwargs
)

if 'install' in sys.argv:
    pwd = os.path.dirname(os.path.abspath(__file__))
    man_path = '/usr/share/man/man7/'
    if os.path.exists(man_path):
        print "Installing man pages"
        path = "%s/aclhound/doc/aclhound.7" % pwd
        input_file = file(path).read()
        ouput_file = file(man_path + 'aclhound.7', 'wa')
        ouput_file.write(input_file)
