#!/usr/bin/env python2.7
# Copyright (C) 2016 Vladimir Lazarenko <favoretti@gmail.com>
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
Upload ACLs to JunOS devices

The following process is followed to ensure zero impact

    upload new ACL via SFTP
    load new ACL via SSH

"""

from Exscript.util.interact import read_login
from Exscript.protocols import SSH2, Telnet, Account

import netrc
import paramiko

from pprint import pprint
from aclhound import textfsm
from StringIO import StringIO

from tempfile import NamedTemporaryFile


def deploy(hostname=None, acls=None, transport='ssh', save_config=True,
           timeout=60):
    """
    Deploy code to a JunOS device
    """
    try:
        username, acc, password = \
            netrc.netrc().authenticators(hostname)
        account = Account(name=username, password=password, key=None)
    except Exception, e:
        print e
        print("ERROR: could not find device in ~/.netrc file")
        print("HINT: either update .netrc or enter username + pass now.")
        try:
            account = read_login()
        except EOFError:
            print("ERROR: could not find proper username + pass")
            print("HINT: set username & pass in ~/.netrc for device %s"
                  % hostname)
            import sys
            sys.exit(2)

    def s(conn, line):
        print("   %s" % line)
        conn.execute(line)

    # main flow of the program starts here

    for policy in acls:
        # deal with ipv4 only for now
        if acls[policy]['afi'] == 4:
            f = NamedTemporaryFile(delete=True)
            f.write(acls[policy]['policy'])
            tr = paramiko.Transport((hostname, 22))
            tr.connect(username = username, password = password)

            sftp = paramiko.SFTPClient.from_transport(tr)
            sftp.put(f.name, "./{}".format(policy))
            sftp.close()

            tr.close()
            f.close()

    if transport == 'ssh':
        conn = SSH2(verify_fingerprint=False, debug=1, timeout=timeout)
    elif transport == 'telnet':
        conn = Telnet(debug=0)
    else:
        print("ERROR: Unknown transport mechanism: %s"
              % transport)
        sys.exit(2)
    conn.set_driver('junos')
    conn.connect(hostname)
    conn.login(account)

    conn.execute("cli")
    conn.execute("edit")
    for policy in acls:
        if acls[policy]['afi'] == 4:
            s(conn, "delete {}".format(policy))
            s(conn, "load set {}".format(policy))
            s(conn, "commit")

