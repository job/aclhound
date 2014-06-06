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

import json
import datetime
import ipaddr

now = datetime.date.today()
now_stamp = int(now.strftime('%Y%M%d'))


class Render():
    def __init__(self, **kwargs):
        self.data = []

    def add(self, ast):
        # only add policy to object if it is not expired
        expire = ast[0]['expire']
        if expire:
            if int(expire) <= now_stamp:
                return
        # normalise src & dst port
        self.data.append(ast)

    def output(self, vendor=None, *largs, **kwargs):
        if not vendor:
            print('This class needs a vendor to output data correctly')
            return False
        return getattr(self, 'output_' + vendor)(*largs, **kwargs)

    def output_ciscoios(self, **kwargs):
        return self.data

    def output_ciscoasa(self, **kwargs):
        policy = self.data
        for rule in policy:
            rule = rule[0]
            print rule
            print ""
            for s_port in rule['source']['l4']['ports']:
                for d_port in rule['destination']['l4']['ports']:
                    print "ip access-list test.acl",
                    if rule['action'] == "allow":
                        action = "permit"
                    else:
                        action = "deny"
                    print action,
                    print rule['protocol'],
                    if "ip" in rule['source']['l3']:
                        if ipaddr.IPNetwork(rule['source']['l3']['ip']).prefixlen in [32, 128]:
                            print "host %s" % rule['source']['l3']['ip'],
                        else:
                            print rule['source']['l3']['ip'],
                    else:
                        print "object-group %s" % rule['source']['l3']['include'],
                    print s_port,
                    if "ip" in rule['destination']['l3']:
                        if ipaddr.IPNetwork(rule['destination']['l3']['ip']).prefixlen in [32, 128]:
                            print "host %s" % rule['destination']['l3']['ip'],
                        else:
                            print rule['destination']['l3']['ip'],
                    else:
                        print "object-group %s" % rule['destination']['l3']['include'],
            print ""
        return self.data

    def output_juniper(self, **kwargs):
        return self.data

    def __str__(self):
        return '\n'.join(self.output(vendor=self.vendor, family=self.family))
