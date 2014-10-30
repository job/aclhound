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

from __future__ import print_function, division, absolute_import, unicode_literals

import sys
import unittest

import os
from os.path import dirname, realpath, join

from grako.parsing import * # noqa
from grako.exceptions import * # noqa

from aclhound.parser import grammarParser
from aclhound.aclsemantics import grammarSemantics
from aclhound.render import Render
from aclhound.generate import generate_policy


class TestAclhound(unittest.TestCase):
    def test_00__parse_ebnf_grammar(self):
        grammar_file = 'aclhound/doc/grammar.ebnf'
        grammar = open(grammar_file).read()
        from grako.parser import GrakoGrammarGenerator
        parser = GrakoGrammarGenerator('aclhound', trace=False)
        state = parser.parse(grammar, filename=None)
        self.assertTrue(state)

#    def test_01__asa_create_policies(self):
#
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
