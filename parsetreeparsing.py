#!/usr/bin/env python3
"""
Recursive Decent Parser: Top Down Parser
Output: Parse Object With Parse Tree
"""
from scanner import Scanner
import sys

__author__ = 'rohitmehra'


class Node:
    def __init__(self, name, children_list=None):
        self.name = name
        self.terminal = True
        if children_list:
            self.children = children_list
            self.terminal = False
        else:
            self.children = []

    def add_child(self, child_node):
        if child_node:
            self.children.append(child_node)
            self.terminal = False


class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        self.scanner.parse()  # update tokens and token_objects of scanner object

        self.look_ahead = 0
        self.tree = Node('<program>')
        self.tokens = self.scanner.tokens  # list of string representation of Tokens

    def parse(self):
        self.program()

    def match(self, name):
        matched = self.tokens[self.look_ahead]
        if matched == name or matched.startswith(name):
            # print(matched, name)
            self.look_ahead += 1
            return Node(matched)

        else:
            print("Error: Expected '{}' but got '{}' !! ".format(name, matched))
            sys.exit(0)

    def program(self):
        if self.tokens[self.look_ahead] == 'PROGRAM':
            self.tree.add_child(self.match('PROGRAM'))

            self.tree.add_child(self.declarations())

            self.tree.add_child(self.match('BEGIN'))

            self.tree.add_child(self.statement_sequence())

            self.tree.add_child(self.match('END'))

    def declarations(self):
        if self.tokens[self.look_ahead] == 'VAR':
            declarations = Node('<declarations>')
            declarations.add_child(self.match('VAR'))
            declarations.add_child(self.match('ident'))
            declarations.add_child(self.match('AS'))
            declarations.add_child(self.type())
            declarations.add_child(self.match('SC'))
            declarations.add_child(self.declarations())
            return declarations
        else:
            return

    def type(self):
        type_node = Node('<type>')
        if self.tokens[self.look_ahead] == 'INT':
            type_node.add_child(self.match('INT'))
        elif self.tokens[self.look_ahead] == 'BOOL':
            type_node.add_child(self.match('BOOL'))
        return type_node

    def statement_sequence(self):
        if self.tokens[self.look_ahead].startswith('ident') or self.tokens[self.look_ahead] == 'IF' or \
                        self.tokens[self.look_ahead] == 'WHILE' or self.tokens[self.look_ahead] == 'WRITEINT':
            ss = Node('<statementSequence>')
            ss.add_child(self.statement())
            ss.add_child(self.match('SC'))
            ss.add_child(self.statement_sequence())
            return ss
        else:
            return

    def statement(self):
        s = Node('<statement>')

        if self.tokens[self.look_ahead].startswith('ident'):
            s.add_child(self.assignment())
        elif self.tokens[self.look_ahead] == 'IF':
            s.add_child(self.if_statement())
        elif self.tokens[self.look_ahead] == 'WHILE':
            s.add_child(self.while_statement())
        elif self.tokens[self.look_ahead] == 'WRITEINT':
            s.add_child(self.writeint())
        return s

    def assignment(self):
        assignment = Node('<assignment>')
        if self.tokens[self.look_ahead].startswith('ident'):
            assignment.add_child(self.match('ident'))
            assignment.add_child(self.match('ASGN'))
            if self.tokens[self.look_ahead] == 'READINT':
                assignment.add_child(self.match('READINT'))
            else:
                assignment.add_child(self.expression())
        return assignment

    def if_statement(self):
        if_statement = Node('<ifStatement>')
        if self.tokens[self.look_ahead] == 'IF':
            if_statement.add_child(self.match('IF'))
            if_statement.add_child(self.expression())
            if_statement.add_child(self.match('THEN'))
            if_statement.add_child(self.statement_sequence())
            if_statement.add_child(self.else_clause())
            if_statement.add_child(self.match('END'))
        return if_statement

    def else_clause(self):
        if self.tokens[self.look_ahead] == 'ELSE':
            else_clause = Node('<elseClause>')
            else_clause.add_child(self.match('ELSE'))
            else_clause.add_child(self.statement_sequence())
            return else_clause
        else:
            return

    def while_statement(self):
        while_statement = Node('<whileStatement>')
        if self.tokens[self.look_ahead] == 'WHILE':
            while_statement.add_child(self.match('WHILE'))
            while_statement.add_child(self.expression())
            while_statement.add_child(self.match('DO'))
            while_statement.add_child(self.statement_sequence())
            while_statement.add_child(self.match('END'))
        return while_statement

    def writeint(self):
        writeint = Node('<writeInt>')
        if self.tokens[self.look_ahead] == 'WRITEINT':
            writeint.add_child(self.match('WRITEINT'))
            writeint.add_child(self.expression())
        return writeint

    def expression(self):
        expression = Node('<expression>')
        if self.tokens[self.look_ahead].startswith('ident') or self.tokens[self.look_ahead].startswith(
                'num') or self.tokens[self.look_ahead].startswith('boollit') or self.tokens[self.look_ahead] == 'LP':
            expression.add_child(self.simple_expression())
            if self.tokens[self.look_ahead].startswith('COMPARE'):
                expression.add_child(self.match('COMPARE'))
                expression.add_child(self.expression())
        return expression

    def simple_expression(self):
        simple_expression = Node('<simpleExpression>')
        if self.tokens[self.look_ahead].startswith('ident') or self.tokens[self.look_ahead].startswith(
                'num') or self.tokens[self.look_ahead].startswith('boollit') or self.tokens[self.look_ahead] == 'LP':
            simple_expression.add_child(self.term())
            if self.tokens[self.look_ahead].startswith('ADDITIVE'):
                simple_expression.add_child(self.match('ADDITIVE'))
                simple_expression.add_child(self.simple_expression())
        return simple_expression

    def term(self):
        term = Node('<term>')
        if self.tokens[self.look_ahead].startswith('ident') or self.tokens[self.look_ahead].startswith(
                'num') or self.tokens[self.look_ahead].startswith('boollit') or self.tokens[self.look_ahead] == 'LP':
            term.add_child(self.factor())
            if self.tokens[self.look_ahead].startswith('MULTIPLICATIVE'):
                term.add_child(self.match('MULTIPLICATIVE'))
                term.add_child(self.term())
        return term

    def factor(self):
        factor = Node('<factor>')
        if self.tokens[self.look_ahead].startswith('ident'):
            factor.add_child(self.match('ident'))

        elif self.tokens[self.look_ahead].startswith('num'):
            factor.add_child(self.match('num'))

        elif self.tokens[self.look_ahead].startswith('boollit'):
            factor.add_child(self.match('boollit'))

        elif self.tokens[self.look_ahead] == 'LP':
            factor.add_child(self.match('LP'))
            factor.add_child(self.simple_expression())
            factor.add_child(self.match('RP'))
        return factor


if __name__ == '__main__':
    scanner = Scanner()
    parser = Parser(scanner)
    parser.parse()
