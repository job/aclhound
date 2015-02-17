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

import datetime
import json
import ipaddr
import itertools

from targets import asa
from targets import ios
from targets import junos

now = datetime.date.today()
now_stamp = int(now.strftime('%Y%M%d'))


class Render():

    def __init__(self, name=None, **kwargs):
        self.data = []
        self.name = name

    """ relevant keys for compression/deduplication:
        AST({
            u'source':
                AST({u'l4': {'ports': ['any']},
                     u'l3': AST({u'ip': [u'any'], })}),
            u'destination':
                AST({u'l4': {'ports': ['any']},
                     u'l3': AST({u'ip': [u'any'], })}),
            u'protocol': u'any',
    """

    """
    [AST({u'action': u'allow', u'source': AST({u'l4': {'ports': ['any']},
    u'l3': {'ip': [u'2a02:898:52:ffff::/64', u'94.142.241.49/32',
    u'94.142.241.204', u'94.142.241.51', u'94.142.241.52/32',
    u'94.142.241.54/32']}}), u'destination': AST({u'l4': AST({u'include': None,
                                                              u'ports': [(0,
                                                                          1024)]}),
                                                  u'l3': AST({u'ip': [u'any'],
                                                              u'include':
                                                              None})}),
    u'protocol': u'tcp', u'keywords': AST({u'comment': None, u'state': None,
                                           u'expire': None, u'log': None})})]
    """

    def add(self, ast):
        # only add policy to object if it is not expired
        expire = ast[0]['keywords']['expire']
        if expire:
            if int(expire) <= now_stamp:
                return

        # convert protocol 'tcpudp' to two entries
        if ast[0]['protocol'] == "tcpudp":
            for protocol in ["tcp", "udp"]:
                # because grako's AST() replaced __setitem__ with 'add'
                # functionality, a copy is created and modified
                ast_copy = {}
                for key in ["action", "source", "destination", "keywords"]:
                    ast_copy[key] = ast[0][key]
                ast_copy['protocol'] = protocol
                self.data.append([ast_copy])
            return

        # no special operations apply, just add it
        self.data.append(ast)

    def output(self, vendor=None, afi=None):
        if not vendor:
            print('This class needs a vendor to output data correctly')
            return False
        return getattr(self, 'output_' + vendor)(afi=afi)

    def output_ios(self, **kwargs):
        return ios.render(self, **kwargs)

    def output_asa(self, **kwargs):
        return asa.render(self, **kwargs)

    def output_junos(self, **kwargs):
        return junos.render(self, **kwargs)

#    def __str__(self):
#        return '\n'.join(self.output(vendor=self.vendor, afi=self.afi))
