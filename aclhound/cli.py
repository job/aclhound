#!/usr/bin/env python2.7
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

from __future__ import print_function, division, absolute_import, unicode_literals

import sys
import os

from os.path import dirname, realpath, join

from grako.parsing import * # noqa
from grako.exceptions import * # noqa

from aclhound.parser import grammarParser
from aclhound.aclsemantics import grammarSemantics
from aclhound.render import Render


def parse_policy(filename, startrule='start', trace=False, whitespace=None):

    seen = [filename]

    def walk_file(filename, seen=[], policy=[]):
        try:
            f = open(join(filename)).read().splitlines()
        except IOError:
            print("filename %s referenced in %s does not exist"
                  % (filename, seen[-1]))
            sys.exit()
        for line in f:
            if line.startswith('@'):
                filename = "policy/%s" \
                    % line.split('#')[0][1:]
                if filename not in seen:
                    seen.append(filename)
                    policy = policy + walk_file(filename, seen, policy)
            elif line.startswith(('allow', 'deny')) and line not in policy:
                policy.append(line)
        return policy

    parser = grammarParser(parseinfo=False, semantics=grammarSemantics())
    acl = Render(name="test")
    for line in walk_file(filename, seen):
        ast = parser.parse(line, startrule)
        acl.add(ast)
    output = "\n".join(acl.output(vendor="ciscoasa"))
    return output


def main():
    print('assessing changes ... ')
    if sys.argv[-1] == 'init':
        print("""
git clone ssh://gerrit.ecg.so:29418/ecg-networking
cd ecg-networking
git review --setup -v
git checkout -B $project_name
git add files
git commit""")
        sys.exit()

    if sys.argv[-1] == 'help':
        print("""
To submit a patchset for review do the following steps
* change files
* git add *
* git commit -a
* git-review -v
""")
        sys.exit()

    if sys.argv[-1] == 'build':
        output = parse_policy('policy/management.acl')
        print(output)
        f = open('/opt/firewall-configs/testasa.asa', 'w')
        f.write(output)
        f.write('\n')
        f.close()
        sys.exit(0)
