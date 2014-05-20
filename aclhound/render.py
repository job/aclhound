#!/usr/bin/env python2.7
# Job Snijders - 2014

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
            if rule['source']['l4'] == "any":
                    s_port = ['any']
            for s_port in rule['destination']['l4']['ports']:
                if rule['destination']['l4']['ports'] == "any":
                    d_port = ['any']
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
                    print d_port

            print ""
        return self.data

    def output_juniper(self, **kwargs):
        return self.data

    def __str__(self):
        return '\n'.join(self.output(vendor=self.vendor, family=self.family))
