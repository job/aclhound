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

import ipaddr
from grako.contexts import Closure


def render(self, **kwargs):
    policy = self.data
    config_blob = []

    for rule in policy:
        rule = rule[0]
        s_hosts = rule['source']['l3']['ip']
        d_hosts = rule['destination']['l3']['ip']

        # deal with ICMP
        if "icmp" in rule['protocol']:
            policy = rule['protocol']['icmp']
            if not isinstance(policy, Closure):
                policy = [policy]
            for entry in policy:
                for s_host in s_hosts:
                    for d_host in d_hosts:
                        if rule['action'] == "allow":
                            action = "permit"
                        else:
                            action = "deny"
                        line = "access-list %s extended %s icmp " \
                            % (self.name, action)
                        line += "%s %s " % (s_host, d_host)
                        if entry == u'any':
                            continue
                        else:
                            line += "%s %s" \
                                % (entry['icmp_type'], entry['icmp_code'])
                    config_blob.append(line)
            # jump out of the loop because we have nothing to do with
            # L4 when doing ICMP
            continue

        # layer 3 and 4
        s_ports = rule['source']['l4']['ports']
        d_ports = rule['destination']['l4']['ports']

        for s_port in s_ports:
            for d_port in d_ports:
                for s_host in s_hosts:
                    for d_host in d_hosts:
                        line = "access-list %s extended " % self.name
                        if rule['action'] == "allow":
                            action = "permit "
                        else:
                            action = "deny "
                        line += action
                        line += rule['protocol'] + " "

                        if s_host == u'any':
                            line += "any "
                        elif ipaddr.IPNetwork(s_host).prefixlen in [32, 128]:
                            line += "host %s " % s_host
                        else:
                            line += s_host + " "

                        if s_port != u"any":
                            line += str(s_port) + " "

                        if d_host == u'any':
                            line += "any "
                        elif ipaddr.IPNetwork(d_host).prefixlen in [32, 128]:
                            line += "host %s " % d_host
                        else:
                            line += d_host + " "

                        if d_port != u"any":
                            line += str(d_port) + " "

                        if line not in config_blob:
                            config_blob.append(line)
    return config_blob