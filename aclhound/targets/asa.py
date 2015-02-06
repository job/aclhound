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

from ipaddr import IPNetwork
from grako.contexts import Closure

#FIXME figure out extended versus standard access-lists
#FIXME deal with deny any any any which ASA compresses

def render(self, **kwargs):
    policy = self.data
    afi = kwargs['afi']
    config_blob = []

    def afi_match(host):
        if host == "any":
            return True
        elif IPNetwork(host).version == afi:
            return True
        else:
            return False

    for rule in policy:
        rule = rule[0]
        s_hosts = rule['source']['l3']['ip']
        d_hosts = rule['destination']['l3']['ip']
        stateful = rule['keywords']['state']
        logging = rule['keywords']['log']

        # deal with ICMP
        if "icmp" in rule['protocol']:
            policy = rule['protocol']['icmp']
            # FIXME this should happen in render or aclsemantics
            if not isinstance(policy, Closure):
                policy = [policy]

            # cycle through all ICMP related elements in the AST
            for entry in policy:
                for s_host in s_hosts:
                    if not afi_match(s_host):
                        continue
                    for d_host in d_hosts:
                        if not afi_match(d_host):
                            continue
                        if rule['action'] == "allow":
                            action = "permit"
                        else:
                            action = "deny"
                        extended = "extended " if afi == 4 else ""
                        yes_v6 = "ipv6 " if afi == 6 else ""
                        line = "%saccess-list %s %s%s icmp" \
                            % (yes_v6, self.name + "-v%s" % afi,
                               extended, action)

                        if s_host == u'any':
                            line += " any"
                        elif IPNetwork(s_host).prefixlen in [32, 128]:
                            line += " host %s" % s_host.split('/')[0]
                        # IPv4 must be with netmask, IPv6 in CIDR notation
                        elif afi == 4:
                            line += " %s" % IPNetwork(s_host).with_netmask.replace('/', ' ')
                        else:
                            line += " " + s_host

                        if d_host == u'any':
                            line += " any"
                        elif IPNetwork(d_host).prefixlen in [32, 128]:
                            line += " host %s" % d_host.split('/')[0]
                        # IPv4 must be with netmask, IPv6 in CIDR notation
                        elif afi == 4:
                            line += " %s" % IPNetwork(d_host).with_netmask.replace('/', ' ')
                        else:
                            line += " " + d_host

                        if not entry['icmp_type'] == "any":
                            line += " " + str(entry['icmp_type'])

                        if logging:
                            line += " log"

                        if line not in config_blob:
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
                    if not afi_match(s_host):
                        continue
                    for d_host in d_hosts:
                        if not afi_match(d_host):
                            continue
                        extended = "extended " if afi == 4 else ""
                        yes_v6 = "ipv6 " if afi == 6 else ""
                        line = "%saccess-list %s %s" \
                            % (yes_v6, self.name + "-v%s" % afi, extended)
                        if rule['action'] == "allow":
                            action = "permit"
                        else:
                            action = "deny"
                        line += action
                        if rule['protocol'] == "any":
                            line += " ip"
                        else:
                            line += " " + rule['protocol']

                        if s_host == u'any':
                            line += " any"
                        elif IPNetwork(s_host).prefixlen in [32, 128]:
                            line += " host %s" % s_host.split('/')[0]
                        # IPv4 must be with netmask, IPv6 in CIDR notation
                        elif afi == 4:
                            line += " %s" % IPNetwork(s_host).with_netmask.replace('/', ' ')
                        else:
                            line += " " + s_host

                        if type(s_port) == tuple:
                            line += " range %s %s" % (s_port[0], s_port[1])
                        elif not s_port == "any":
                            line += " eq %s" % str(s_port)

                        if d_host == u'any':
                            line += " any"
                        elif IPNetwork(d_host).prefixlen in [32, 128]:
                            line += " host %s" % d_host.split('/')[0]
                        # IPv4 must be with netmask, IPv6 in CIDR notation
                        elif afi == 4:
                            line += " %s" % IPNetwork(d_host).with_netmask.replace('/', ' ')
                        else:
                            line += " " + d_host

                        if type(d_port) == tuple:
                            line += " range %s %s" % (d_port[0], d_port[1])
                        elif not d_port == "any":
                            line += " eq %s" % str(d_port)

                        if stateful and rule['protocol'] == "tcp":
                            line += " established"

                        if logging:
                            line += " log"

                        if line not in config_blob:
                            config_blob.append(line)

    # add final deny any any at the end of each policy
    extended = "extended " if afi == 4 else ""
    yes_v6 = "ipv6 " if afi == 6 else ""
    line = "%saccess-list %s %sdeny ip any any" \
        % (yes_v6, self.name + "-v%s" % afi, extended)
    config_blob.append(line)
    return config_blob
