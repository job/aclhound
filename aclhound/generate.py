#!/usr/bin/env python2.7
# Copyright (C) 2014-2015 Job Snijders <job@instituut.net>
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
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import sys

from aclhound.aclsemantics import grammarSemantics
from aclhound.parser import grammarParser
from aclhound.render import Render


def generate_policy(filename, startrule='start', trace=False, whitespace=None,
                    afi=4, vendor=None):
    """
    Open a file, run it through the parser, recurse if needed
    Output resembles what you would expect in running-config.
    """

    safe_letters = "abcdefghijklmnopqrstuvwxyz0123456789-_"

    def check_name(name):
        for letter in name:
            if not letter in safe_letters:
                print("ERROR: invalid policy filename: %s" % name)
                sys.exit(2)
        return name

    policy_name = check_name(filename)
    seen = [filename]

    def walk_file(filename, seen=[], policy=[]):
        try:
            f = open("policy/%s" % filename).read().splitlines()
        except IOError:
            print("filename %s referenced in %s does not exist"
                  % (filename, seen[-1]))
            print("HINT: ensure you are in your ACLHound data directory")
            sys.exit()
        for line in f:
            if line.startswith('@'):
                filename = line.split('#')[0][1:]
                if not filename in seen:
                    seen.append(filename)
                    policy = walk_file(filename, seen, policy)
            elif line.startswith(('allow', 'deny')) and line not in policy:
                policy.append(line)
        return policy

    parser = grammarParser(parseinfo=False, semantics=grammarSemantics())
    acl = Render(name=policy_name)
    for line in walk_file(filename, seen):
        ast = parser.parse(line, startrule)
        acl.add(ast)
    output = "\n".join(acl.output(vendor=vendor, afi=afi))
    return output
