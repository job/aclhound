#!/usr/bin/env python
# Job Snijders - 2014

from __future__ import print_function, division, absolute_import, unicode_literals
from grako.parsing import * # noqa
from grako.exceptions import * # noqa

from parser import grammarParser
from aclsemantics import grammarSemantics
from render import Render


def main(filename, startrule, trace=False, whitespace=None):
    f = open(filename)
    parser = grammarParser(parseinfo=False, semantics=grammarSemantics())
    acl = Render()
    for line in f.readlines():
        if line.startswith(('allow', 'deny')):
            ast = parser.parse(line, startrule)
            acl.add(ast)

    print(acl.output(vendor="cisco"))

if __name__ == '__main__':
    main('test.acl', 'start')
