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


def compress_ports_to_range(ports):
    for a, b in itertools.groupby(enumerate(i), lambda(x, y): y - x):
        b = list(b)
        yield b[0][1], b[-1][1]


class Render():

    def __init__(self, name=None, **kwargs):
        self.data = []
        self.name = name

    def add(self, ast):
        # only add policy to object if it is not expired
        expire = ast[0]['expire']
        if expire:
            if int(expire) <= now_stamp:
                return
        # compress port ranges
        #
        #print ast
        # FIXME normalise src & dst port

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
