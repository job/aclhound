#!/usr/bin/env python2.7
# Job Snijders - 2014


class Render():
    def __init__(self, **kwargs):
        self.data = []

    def add(self, ast):
        self.data.append(ast)

    def output(self, vendor=None, *largs, **kwargs):
        if not vendor:
            print('This class needs a vendor to output data correctly')
            return False
        return getattr(self, 'output_' + vendor)(*largs, **kwargs)

    def output_cisco(self, **kwargs):
        return self.data

    def __str__(self):
        return '\n'.join(self.output(vendor=self.vendor, family=self.family))
