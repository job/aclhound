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

"""
Upload ACLs to Cisco ASA devices

WARNING: this does not work on ASA 9.1.2 or higher

The following process is followed to ensure zero impact

    remove old ACL from interface(s)
    remove old ACL from device
    upload new ACL to device
    apply new ACL to interface(s)

"""

from Exscript.util.interact import read_login
from Exscript.protocols import SSH2, Telnet, Account
from Exscript.protocols.Exception import LoginFailure

import netrc

from pprint import pprint
from aclhound import textfsm
from StringIO import StringIO


def deploy(hostname=None, acls=None, transport='ssh', save_config=False):
    """
    Deploy code in a safe way o a Cisco IOS device.
    """

    try:
        username, enable_pass, password = \
            netrc.netrc().authenticators(hostname)
        account = Account(name=username, password=password,
                          password2=enable_pass)
    except:
        account = read_login()

    def s(conn, line):
        print("   %s" % line)
        conn.execute(line)

    def collect_interfaces(conn):
        template = """# textfsm
Value Required Aclname ([^ ]+)
Value Required Direction ([^ ]+)
Value Required Interface (.*)

Start
  ^access-group ${Aclname} ${Direction} interface ${Interface} -> Record Start

"""
        template_file = StringIO(template)
        table = textfsm.TextFSM(template_file)
        conn.execute('show run | include ^access-group')
        map_acl_int = {}
        for aclname, direction, interface in table.ParseText(conn.response):
            if aclname in map_acl_int.keys():
                map_acl_int[aclname].append({"dir": direction,
                                             "int": interface})
            else:
                map_acl_int[aclname] = [{"dir": direction, "int": interface}]

        return map_acl_int

    # main flow of the program starts here
    if transport == 'ssh':
        conn = SSH2(verify_fingerprint=False, debug=0)
    elif transport == 'telnet':
        conn = Telnet(debug=0)
    else:
        print("ERROR: Unknown transport mechanism: %s" %
              transport)
        sys.exit(2)
    conn.set_driver('ios')
    conn.connect(hostname)
    try:
        conn.login(account)
    except LoginFailure:
        print("ERROR: Username or Password incorrect for %s" % hostname)
        print("HINT: verify authentication details in your .netrc file")
        sys.exit(2)
    s(conn, "terminal pager 0")

    map_pol_int = collect_interfaces(conn)
    pprint(map_pol_int)

    def lock_step(lock, pol):
        name = acls[pol]['name']
        afi = acls[pol]['afi']
        policy = acls[pol]['policy']
        print("INFO: uploading name: %s, afi: %s" % (name, afi))
        s(conn, 'configure terminal')
        if afi == 4:
            try:
                s(conn, "clear configure access-list %s%s" % (lock, name))
            except:
                pass
            for line in policy.split('\n'):
                if lock:
                    line = line.replace("access-list %s " % name,
                                        "access-list %s%s " % (lock, name))
                s(conn, line)
        if afi == 6:
            try:
                s(conn, "clear configure ipv6 access-list %s%s" % (lock, name))
            except:
                pass
            for line in policy.split('\n'):
                if lock:
                    line = line.replace("access-list %s " % name,
                                        "access-list %s%s " % (lock, name))
                s(conn, line)
        s(conn, "end")

        # then replace ACL on all interfaces / VTYs
        if name in map_pol_int:
            for entry in map_pol_int[name]:
                print("INFO: lockstepping policy %s afi %s" % (name, afi))
                s(conn, "configure terminal")
                s(conn, "access-group %s%s %s interface %s"
                  % (lock, name, entry['dir'], entry['int']))
                s(conn, "end")

    for policy in acls:
        for lock in ["LOCKSTEP-", ""]:
            lock_step(lock, policy)
        # cleanup
        s(conn, "configure terminal")
        if acls[policy]['afi'] == 4:
            s(conn, "clear configure access-list LOCKSTEP-%s"
              % acls[policy]['name'])
        if acls[policy]['afi'] == 6:
            s(conn, "clear configure ipv6 access-list LOCKSTEP-%s"
              % acls[policy]['name'])
        s(conn, "end")
    if save_config == True:
        s(conn, "write")

