#!/usr/bin/env python
# Job Snijders - 2014

from __future__ import print_function, division, absolute_import, unicode_literals
from grako.parsing import * # noqa
from grako.exceptions import * # noqa

from parser import grammarParser
from aclsemantics import grammarSemantics
from render import Render
from pprint import pprint

def main(filename, startrule, trace=False, whitespace=None):
    f = open(filename)
    parser = grammarParser(parseinfo=False, semantics=grammarSemantics())
    acl = Render()
    for line in f.readlines():
        if line.startswith(('allow', 'deny')):
            ast = parser.parse(line, startrule)
            acl.add(ast)
    import json
    print(json.dumps(acl.output(vendor="ciscoios"), indent=2))

if __name__ == '__main__':
    main('test.acl', 'start')
