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
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from grako.exceptions import FailedSemantics
from parser import grammarParser

import ipaddr
import itertools
import re
import sys


class grammarSemantics(object):

    def start(self, ast):
        return ast

    def rule(self, ast):
        return ast

    def optional_keywords(self, ast):
        return ast

    def state_expr(self, ast):
        if not self._protocol == "tcp":
            raise FailedSemantics('Only TCP entries can be stateful')
        if ast == "stateful":
            return True
        else:
            return False

    def log_expr(self, ast):
        if ast == "log":
            return True
        else:
            return False

    def expire_expr(self, ast):
        return ast

    def date(self, ast):
        return ast

    def icmp_expr(self, ast):
        return ast

    def icmp_code(self, ast):
        return ast

    def icmp_number(self, ast):
        if 0 <= int(ast) < 255:
            return int(ast)
        else:
            raise FailedSemantics('ICMP code/type must be between 0 and 255')

    def icmp_term(self, ast):
        if ast == u'any':
            return {u'icmp_code': u'any', u'include': None,
                    u'icmp_type': u'any'}
        if ast[u'include']:
            icmp_p = []
            includes = []
            object_name = 'objects/%s.icmp' % ast['include']
            includes.append(object_name)
            for include in includes:
                try:
                    file_h = open(include).read().splitlines()
                except IOError:
                    print "ERROR: could not open file: %s" % include
                    sys.exit(2)
                for line in file_h:
                    if line.startswith('@'):
                        include_name = 'objects/%s.icmp' \
                            % line.split('#')[0].strip()[1:]
                        if include_name not in includes:
                            includes.append(include_name)
                    else:
                        icmp_p.append(line.split('#')[0].strip())
            icmp_types = "\n".join(set(icmp_p))
            p = grammarParser(parseinfo=False, semantics=grammarSemantics())
            ast = p.parse(icmp_types, 'icmp_term')
        return ast

    def action_expr(self, ast):
        return ast

    def protocol_expr(self, ast):
        if "icmp" in ast:
            self._protocol = "icmp"
        elif ast in ["tcp", "tcpudp", "udp", "any"]:
            self._protocol = str(ast)
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
        if self._protocol not in ["tcp", "tcpudp", "udp"] and ast['l4'] is not None:
            raise FailedSemantics('Cannot combine layer 4 information (ports) with ICMP protocol')
        if not ast['l4']:
            ast['l4'] = {}
            ast['l4']['ports'] = ["any"]
        return ast

    def endpoint_expr(self, ast):
        # allow recursion in host expressions
        if ast[u'include']:
            hosts = []
            includes = []
            object_name = 'objects/%s.hosts' % ast['include']
            includes.append(object_name)
            for include in includes:
                try:
                    file_h = open(include).read().splitlines()
                except IOError:
                    print "ERROR: could not open file: %s" % include
                    import os
                    print os.getcwd()
                    sys.exit(2)
                for line in file_h:
                    if line.startswith('@'):
                        include_name = 'objects/%s.hosts' \
                            % line.split('#')[0].strip()[1:]
                        if include_name not in includes:
                            includes.append(include_name)
                    else:
                        hosts.append(line.split('#')[0])
            hosts = "\n".join(set(hosts))
            p = grammarParser(parseinfo=False, semantics=grammarSemantics())
            ast = {'ip': p.parse(hosts, 'endpoint_list')}
        return ast

    def group_expr(self, ast):
        return ast

    def portgroup_expr(self, ast):
        return ast

    def port_term(self, ast):
        if ast[u'include']:
            ports = []
            includes = []
            object_name = 'objects/%s.ports' % ast['include']
            includes.append(object_name)
            for include in includes:
                try:
                    file_h = open(include).read().splitlines()
                except IOError:
                    print "ERROR: could not open file: %s" % include
                    sys.exit(2)
                for line in file_h:
                    if line.startswith('@'):
                        include_name = 'objects/%s.ports' \
                            % line.split('#')[0].strip()[1:]
                        if include_name not in includes:
                            includes.append(include_name)
                    else:
                        ports.append(line.split('#')[0])
            ports = "\n".join(set(ports))
            p = grammarParser(parseinfo=False, semantics=grammarSemantics())
            ast = p.parse(ports, 'port_term')
        return ast

    def prefix(self, ast):
        try:
            prefix = ipaddr.IPNetwork(ast)
            if not prefix.ip == prefix.network:
                raise FailedSemantics('Not a valid IP address or prefix!')
        except:
            raise FailedSemantics('Not a valid IP address or prefix!')
        return ast

    def NUMBER(self, ast):
        return int(ast)

    def port_atoms(self, ast):
        ports = []
        """[AST({u'range': [0, 1024], u'single': None})]
        [AST({u'range': [1024, 65535], u'single': None})]
        [AST({u'range': [1023, 65535], u'single': None}),
            AST({u'range': [0, 1022], u'single': None}),
            AST({u'single': 1, u'range': None}),
            AST({u'single': 2, u'range': None}),
            AST({u'single': 3, u'range': None}),
            AST({u'single': 4, u'range': None})]"""

        for atom in ast:
            if atom['single']:
                ports.append(atom['single'])
            if atom['range']:
                low, high = atom['range']
                ports = ports + range(low, high + 1)
        # sort and deduplicate all ports
        ports = set(ports)
        # create the smallest amount of port ranges possible
        atoms = []
        for a, b in itertools.groupby(enumerate(ports), lambda(x, y): y - x):
            b = list(b)
            atoms.append(b[0][1] if b[0][1] == b[-1][1]
                         else (b[0][1], b[-1][1]))
        return list(set(atoms))

    def port_expr(self, ast):
        return ast

    def port_range(self, ast):
        low = 0 if ast[0] == "-" else int(ast[0])
        high = 65535 if ast[1] == "-" else int(ast[1])
        if low > high:
            raise FailedSemantics('First port cannot be higher than second \
port in a range expression')
            sys.exit(2)
        return [low, high]

    def port_number(self, ast):
        if not 0 < ast < 2 ** 16:
            raise FailedSemantics('Port number must be between 0 and 2^16')
        return ast

    def address_string(self, ast):
        return ast

    def endpoint_list(self, ast):
        return ast

    def number(self, ast):
        return ast


if __name__ == '__main__':
    pass
