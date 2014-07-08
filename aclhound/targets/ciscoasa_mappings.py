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

mapping = {}

mapping['tcp'] = {
    7: "echo",
    9: "discard",
    13: "daytime",
    19: "chargen",
    20: "ftp-data",
    21: "ftp",
    22: "ssh",
    23: "telnet",
    25: "smtp",
    43: "whois",
    49: "tacacs",
    53: "domain",
    70: "gopher",
    79: "finger",
    80: "www",
    101: "hostname",
    109: "pop2",
    110: "pop3",
    111: "sunrpc",
    113: "ident",
    119: "nntp",
    139: "netbios-ssn",
    143: "imap4",
    179: "bgp",
    194: "irc",
    389: "ldap",
    443: "https",
    496: "pim-auto-rp",
    512: "exec",
    513: "login",
    514: "cmd",
    515: "lpd",
    517: "talk",
    540: "uucp",
    543: "klogin",
    544: "kshell",
    636: "ldaps",
    750: "kerberos",
    1352: "lotusnotes",
    1494: "citrix-ica",
    1521: "sqlnet",
    1720: "h323",
    1723: "pptp",
    2049: "nfs",
    2748: "ctiqbe",
    5190: "aol",
    5631: "pcanywhere-data"
}

mapping['udp'] = {
    7: "echo",
    9: "discard",
    37: "time",
    42: "nameserver",
    49: "tacacs",
    53: "domain",
    67: "bootps",
    68: "bootpc",
    69: "tftp",
    111: "sunrpc",
    123: "ntp",
    137: "netbios-ns",
    138: "netbios-dgm",
    161: "snmp",
    162: "snmptrap",
    177: "xdmcp",
    195: "dnsix",
    434: "mobile-ip",
    496: "pim-auto-rp",
    500: "isakmp",
    512: "biff",
    513: "who",
    514: "syslog",
    517: "talk",
    520: "rip",
    750: "kerberos",
    1645: "radius",
    1646: "radius-acct",
    2049: "nfs",
    5510: "secureid-udp",
    5632: "pcanywhere-status"
}

mapping['icmp'] = {
    0: "echo-reply",
    3: "unreachable",
    4: "source-quench",
    5: "redirect",
    6: "alternate-address",
    8: "echo",
    9: "router-advertisement",
    10: "router-solicitation",
    11: "time-exceeded",
    12: "parameter-problem",
    13: "timestamp-request",
    14: "timestamp-reply",
    15: "information-request",
    16: "information-reply",
    17: "mask-request",
    18: "mask-reply",
    30: "traceroute",
    31: "conversion-error",
    32: "mobile-redirect"
}

mapping['icmpv6'] = {
    1: "unreachable",
    2: "packet-too-big",
    3: "time-exceeded",
    4: "parameter-problem",
    128: "echo",
    129: "echo-reply",
    130: "membership-query",
    131: "membership-report",
    132: "membership-reduction",
    133: "router-solicitation",
    134: "router-advertisement",
    135: "neighbor-solicitation",
    136: "neighbor-advertisement",
    137: "neighbor-redirect",
    138: "router-renumbering"
}
