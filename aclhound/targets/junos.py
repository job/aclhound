#!/usr/bin/env python2.7
# Copyright (C) 2016-201s65 Vladimir Lazarenko <favoretti@gmail.com>
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
import pprint
import sys

#FIXME figure out extended versus standard access-lists
#FIXME deal with deny any any any which ASA compresses


def render(self, **kwargs):
    policy = self.data
    afi = kwargs['afi']
    config_blob = []

#    if afi == 4:
#        config_blob.append("ip access-list extended %s-v4" % self.name)
#    if afi == 6:
#        config_blob.append("ipv6 access-list %s-v6" % self.name)

    def afi_match(host):
        if host == "any":
            return True
        elif IPNetwork(host).version == afi:
            return True
        else:
            return False

    if afi == 6:
        return config_blob


    config_blob.append("edit firewall filter {} term 1".format(self.name))
    config_blob.append("set from protocol icmp")
    config_blob.append("set then accept")
    config_blob.append("top")

    term_count = 2

    for rule in policy:
        rule = rule[0]
        if "icmp" in rule['protocol']:
            continue
        s_hosts = rule['source']['l3']['ip']
        d_hosts = rule['destination']['l3']['ip']
        logging = rule['keywords']['log']
        stateful = rule['keywords']['state']
        # layer 3 and 4
        s_ports = rule['source']['l4']['ports']
        d_ports = rule['destination']['l4']['ports']
        action = rule['action']
        if action == "allow":
            action = "accept"
        elif action == "deny":
            action == "discard"
        protocol = rule['protocol']
        for s_port in s_ports:
            for d_port in d_ports:
                for s_host in s_hosts:
                    if not afi_match(s_host):
                        continue
                    for d_host in d_hosts:
                        if not afi_match(d_host):
                            continue
                        config_blob.append("edit firewall filter {} term {}".format(self.name, term_count))
                        if protocol != "any":
                            config_blob.append("set from protocol {}".format(protocol))
                        if s_host != "any":
                            config_blob.append("set from source-address {}".format(s_host))
                        if d_host != "any":
                            config_blob.append("set from destination-address {}".format(d_host))
                        if type(s_port) == list:
                            s_port = s_port[0]
                            if type(s_port) == tuple:
                                config_blob.append("set from source-port {}-{}".format(s_port[0], s_port[1]))
                            else:
                                config_blob.append("set from source-port {}".format(s_port))
                        elif s_port != "any":
                            config_blob.append("set from source-port {}".format(str(s_port)))
                        if type(d_port) == list:
                            d_port = d_port[0]
                            if type(d_port) == tuple:
                                config_blob.append("set from destination-port {}-{}".format(d_port[0], d_port[1]))
                            else:
                                config_blob.append("set from destination-port {}".format(d_port))
                        elif d_port != "any":
                            config_blob.append("set from destination-port {}".format(str(d_port)))
                        if action == "accept":
                            config_blob.append("set then accept")
                        elif action == "discard":
                            config_blob.append("set then syslog")
                            config_blob.append("set then discard")
                        config_blob.append("top")
                        term_count = term_count + 1


    config_blob.append("set firewall filter {} term DROP_ALL then syslog".format(self.name))
    config_blob.append("set firewall filter {} term DROP_ALL then discard".format(self.name))
    return config_blob
