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
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from grako.exceptions import FailedSemantics
from grako.grammars import ModelContext

import ipaddr

class grammarSemantics(object):
    def __init__(self):
        self._protocol = None

    def start(self, ast):
        return ast

    def rule(self, ast):
        return ast

    def state_expr(self, ast):
        return ast

    def expire_expr(self, ast):
        return ast

    def date(self, ast):
        return ast

    def icmp_parameter(self, ast):
        if not ast:
            return "any"
        if 0 <= int(ast) < 255:
            return int(ast)
        else:
            raise FailedSemantics('ICMP code/type must be between 0 and 255')

    def action_expr(self, ast):
        return ast

    def protocol_expr(self, ast):
        if "icmp" in ast:
            self._protocol = "icmp"
        elif ast == u'udp':
            self._protocol = "udp"
        elif ast == u'tcp':
            self._protocol = "tcp"
        elif ast == u'any':
            self._protocol = "any"
        else:
            raise FailedSemantics('No idea what protocol we are dealing with here')
        return ast

    def comment_expr(self, ast):
        return ast

    def string(self, ast):
        return ast

    def source_expr(self, ast):
        return ast

    def dst_expr(self, ast):
        return ast

    def endpoint_tuple(self, ast):
        # when port specifications are omitted any is assumed
        if self._protocol not in ["tcp", "udp"] and ast['l4'] is not None:
            raise FailedSemantics('Cannot combine layer 4 information (ports) with ICMP protocol')
        if not ast['l4']:
            ast['l4'] = {}
            ast['l4']['ports'] = ["any"]
        return ast

    def endpoint_expr(self, ast):
        return ast

    def group_expr(self, ast):
        return ast

    def portgroup_expr(self, ast):
        return ast

    def port_term(self, ast):
        return ast

    def prefix(self, ast):
        try:
            ipaddr.IPNetwork(ast)
        except:
            raise FailedSemantics('Not a valid IP address or prefix!')
        return ast

    def NUMBER(self, ast):
        return ast

    def port_atoms(self, ast):
        ports = []
        """[u'80']
        [u'5000']
        [AST({u'range': [u'1', u'10']})]
        [AST({u'range': [u'5', u'10']})]
        [u'1']
        [u'2', AST({u'range': [u'1', u'2']}), u'4']
        [u'1']
        [u'2', u'2', u'3', u'4']"""
        for atom in ast:
            if 'single' in atom:
                ports.append(int(atom['single']))
            if 'range' in atom:
                low, high = map(int, atom['range'])
                ports = ports + range(low, high + 1)
        return list(set(ports))

    def port_expr(self, ast):
        return ast

    def port_range(self, ast):
        low, high = map(int, ast)
        if low > high:
            raise FailedSemantics('First port cannot be higher than second \
port in a range expression')
            pass
        return ast

    def port_number(self, ast):
        port = int(ast)
        if not 0 < port < 2 ** 16:
            raise FailedSemantics('Port number must be between 0 and 2^16')
        return ast

if __name__ == '__main__':
    pass
