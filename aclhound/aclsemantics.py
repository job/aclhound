#!/usr/bin/env python

from grako.exceptions import FailedParse
from grako.buffering import Buffer

class grammarSemantics(object):
    def start(self, ast):
        return ast

    def rule(self, ast):
        return ast

    def state_expr(self, ast):
        return ast

    def expire_expr(self, ast):
        return ast

    def date(self, ast):
        return ast

    def action_expr(self, ast):
        return ast

    def protocol_expr(self, ast):
        return ast

    def comment_expr(self, ast):
        return ast

    def string(self, ast):
        return ast

    def source_expr(self, ast):
        return ast

    def dst_expr(self, ast):
        return ast

    def endpoint_tuple(self, ast):
        return ast

    def endpoint_expr(self, ast):
        return ast

    def group_expr(self, ast):
        return ast

    def portgroup_expr(self, ast):
        return ast

    def port_term(self, ast):
        return ast

    def prefix(self, ast):
        return ast

    def number(self, ast):
        return ast

    def NUMBER(self, ast):
        return ast

    def port_atoms(self, ast):
        return ast

    def port_expr(self, ast):
        return ast

    def port_range(self, ast):
        # low, high = map(int, ast.split('-'))
        # if low > high:
        # print(Buffer(ast).line_info(ast))
        return ast

    def port_number(self, ast):
        return ast

if __name__ == '__main__':
    pass
