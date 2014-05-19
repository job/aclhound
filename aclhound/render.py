#!/usr/bin/env python2.7
# Job Snijders - 2014

import json
import datetime

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
        import json
#        print(json.dumps(self.data, indent=2))
        return self.data

    def output_ciscoasa(self, **kwargs):
        return self.data

    def output_juniper(self, **kwargs):
        return self.data


    def __str__(self):
        return '\n'.join(self.output(vendor=self.vendor, family=self.family))
