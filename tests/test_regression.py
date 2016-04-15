#!/usr/bin/env python
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
# ARISING IN ANY WAY OUT OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import print_function, division, absolute_import, unicode_literals

import sys
import unittest

import os

from grako.parsing import * # noqa
from grako.exceptions import * # noqa

from aclhound.cli import ACLHoundClient

from cStringIO import StringIO


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self._stringio.write('EXCEPTION RAISED')
        self.extend(self._stringio.getvalue().splitlines())
        sys.stdout = self._stdout
        return True  # Ignore any exception


class TestAclhound(unittest.TestCase):
    def test_00__parse_ebnf_grammar(self):
        grammar_file = 'aclhound/doc/grammar.ebnf'
        grammar = open(grammar_file).read()
        from grako.parser import GrakoGrammarGenerator
        parser = GrakoGrammarGenerator('aclhound', trace=False)
        state = parser.parse(grammar, filename=None)
        self.assertTrue(state)

    def test_01__build_ios(self):
        os.environ["WORKSPACE"] = os.getcwd() + "/tests/data"
        with Capturing() as output:
            cli = ACLHoundClient({u'--help': False, u'--version': False,
                                  u'<args>': ['all'], u'<command>': 'build',
                                  u'debug': False, u'jenkins': True})
            cli.build({u'--help': False, u'--version': False, u'<devicename>':
                       'devices/s2-ios.meerval.net', u'<command>': 'build',
                       u'debug': False, u'jenkins': True})
        self.assertNotIn('ERROR', '\n'.join(output))
        predefined_output = open('build_ios.txt').read().splitlines()
        # remove first line, as this contains system specific output
        output.pop(0)
        predefined_output.pop(0)
        output = "\n".join(output)
        predefined_output = "\n".join(predefined_output)
        # compare generated & predefined output blob, should be same
        self.maxDiff = None
        self.assertEquals(output, predefined_output)

    def test_02__build_asa(self):
        os.environ["WORKSPACE"] = os.getcwd()
        with Capturing() as output:
            cli = ACLHoundClient({u'--help': False, u'--version': False,
                                  u'<args>': ['all'], u'<command>': 'build',
                                  u'debug': False, u'jenkins': True})
            cli.build({u'--help': False, u'--version': False, u'<devicename>':
                       'devices/s2-asa.meerval.net', u'<command>': 'build',
                       u'debug': False, u'jenkins': True})
        self.assertNotIn('ERROR', '\n'.join(output))
        predefined_output = open('build_asa.txt').read().splitlines()
        output.pop(0)
        predefined_output.pop(0)
        output = "\n".join(output)
        predefined_output = "\n".join(predefined_output)
        self.maxDiff = None
        self.assertEquals(output, predefined_output)

    def test_03__build_junos(self):
        os.environ["WORKSPACE"] = os.getcwd()
        with Capturing() as output:
            cli = ACLHoundClient({u'--help': False, u'--version': False,
                                  u'<args>': ['all'], u'<command>': 'build',
                                  u'debug': False, u'jenkins': True})
            cli.build({u'--help': False, u'--version': False, u'<devicename>':
                       'devices/junos.eby', u'<command>': 'build',
                       u'debug': False, u'jenkins': True})
        predefined_output = open('build_junos.txt').read().splitlines()
        output.pop(0)
        predefined_output.pop(0)
        output = "\n".join(output)
        predefined_output = "\n".join(predefined_output)
        self.maxDiff = None
        self.assertEquals(output, predefined_output)

    def test_04__deploy_ios(self):
        if not "TRAVIS" in os.environ:
            self.skipTest("Not inside Travis")
            return
        elif not os.environ["TRAVIS_REPO_SLUG"] == "job/aclhound":
            self.skipTest("Skipping this test when triggered by a fork")
            return
        os.environ["WORKSPACE"] = os.getcwd()
        with Capturing() as output:
            cli = ACLHoundClient({u'--help': False, u'--version': False,
                                  u'<args>': ['all'], u'<command>': 'deploy',
                                  u'debug': False, u'jenkins': True})
            cli.deploy({u'--help': False, u'--version': False, u'<devicename>':
                        'devices/steffann.mu.meerval.net',
                        u'<command>': 'deploy', u'debug': False,
                        u'jenkins': True})
#        predefined_output = open('deploy_ios.txt').read().splitlines()
#        output = "\n".join(output)
#        predefined_output = "\n".join(predefined_output)
#        self.maxDiff = None
#        self.assertEquals(output, predefined_output)

#        self.assertTrue(parse_examples('policy/generic_policy'))
#        self.assertTrue(True)
#        tree = radix.Radix()
#        self.assertTrue('radix.Radix' in str(type(tree)))
#        del tree
#        self.assertEquals(num_nodes_in - num_nodes_del, num_nodes_out)
#        self.assertNotEquals(node, None)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
