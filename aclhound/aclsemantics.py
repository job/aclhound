#!/usr/bin/env python

from grako.exceptions import FailedSemantics
import ipaddr

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
        # when port specifications are omitted any is assumed
        if not ast['l4']:
            ast['l4'] = {}
            ast['l4']['ports'] = ["any"]
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
        try:
            ipaddr.IPNetwork(ast)
        except:
            raise FailedSemantics('Not a valid IP address or prefix!')
        return ast

    def NUMBER(self, ast):
        return ast

    def port_atoms(self, ast):
        ports = []
        """[u'80']
        [u'5000']
        [AST({u'range': [u'1', u'10']})]
        [AST({u'range': [u'5', u'10']})]
        [u'1']
        [u'2', AST({u'range': [u'1', u'2']}), u'4']
        [u'1']
        [u'2', u'2', u'3', u'4']"""
        for atom in ast:
            if 'single' in atom:
                ports.append(int(atom['single']))
            if 'range' in atom:
                low, high = map(int, atom['range'])
                ports = ports + range(low, high + 1)
        return list(set(ports))

    def port_expr(self, ast):
        return ast

    def port_range(self, ast):
        low, high = map(int, ast)
        if low > high:
            raise FailedSemantics('First port cannot be higher than second \
port in a range expression')
            pass
        return ast

    def port_number(self, ast):
        port = int(ast)
        if not 0 < port < 2 ** 16:
            raise FailedSemantics('Port number must be between 0 and 2^16')
        return ast

if __name__ == '__main__':
    pass
