#!/usr/bin/env python3
"""
Recursive Decent Parser: Top Down Parser with type checking
AST: Tree of type checked Objects
"""
import sys
from scanner import Scanner

__author__ = 'rohitmehra'


class AST:
    pass


class Num(AST):
    def __init__(self, token):  # token.type = num, token.value = some_number
        self.value = int(token.value)
        self.type = 'int'

    def __str__(self):
        return str(self.value) + ':' + self.type


class Bool(AST):
    def __init__(self, token):  # token.type = boollit, token.value = true/false
        # self.value = bool(token.value[0].upper() + token.value[1:])
        self.value = token.value
        self.type = 'bool'

        # if self.value:
        #     self.value = 1
        # else:
        #     self.value = 0

    def __str__(self):
        return str(self.value).lower() + ':' + self.type


class Variable(AST):
    def __init__(self, ident_token, type_token):
        self.name = ident_token.value  # identifier name
        self.type = type_token.type.lower()  # declared type
        self.value = None

    def __str__(self):
        return str(self.name + ':' + self.type)


class ReadInt(AST):
    def __init__(self):
        self.type = 'int'
        self.value = None

    def __str__(self):
        return 'readInt' + ':' + self.type


class WriteInt:
    def __init__(self, node):
        self.child = node
        self.type = 'int'

    def __str__(self):
        return 'writeInt' + ':' + self.type


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left  # left node
        self.token = self.op = op  # op token
        self.right = right  # right node
        self.type = 'int'
        self.color = 'white'  # will turn indianred1 when lhs, rhs type mismatch (rm)

    def __str__(self):
        if self.color == 'white':
            return self.op.value + ':' + self.type
        else:
            return self.op.value


class AssignOp(BinOp):
    def __str__(self):
        return self.op.value


class CompareOp(BinOp):
    def __init__(self, left, op, right):
        super(CompareOp, self).__init__(left, op, right)
        self.type = 'bool'

    def __str__(self):
        if self.color == 'white':
            return self.op.value + ':' + 'bool'
        else:
            return self.op.value


class WhileOp:
    def __init__(self, compareOp, statement_block):
        self.name = 'while'
        self.comparision = compareOp
        self.statements = statement_block


class IfOp:  # compare, then statements, else statements
    def __init__(self, compareOp, if_block, else_block):
        self.name = 'if'
        self.comparision = compareOp
        self.if_statements = if_block
        self.else_statements = else_block


class Block(AST):
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, child_node):
        if child_node:
            self.children.append(child_node)


class Statements(Block):
    pass


class Declarations(Block):
    pass


class Program(Block):
    pass


class Parser:
    def __init__(self, scanner):  # needs scanner object
        self.scanner = scanner
        self.scanner.parse()  # update tokens and token_objects of scanner object

        self.look_ahead = 0  # lookahead pointer
        self.tokens = self.scanner.tokens  # list of string representation of Tokens (rm)
        self.token_objects = self.scanner.token_objects  # list of token objects
        self.variable_map = {}  # for type checking
        self.tree = Program('<program>')
        self.declarationList = Declarations('<declarations>')

    def parse(self):
        try:
            self.program()
        except AttributeError as e:
            sys.exit(0)

    def match(self, name):
        matched = self.tokens[self.look_ahead]
        if matched == name or matched.startswith(name):
            self.look_ahead += 1

        else:
            print("Error: Expected '{}' but got '{}' !! ".format(name, matched))
            sys.exit(0)

    def program(self):
        if self.tokens[self.look_ahead] == 'PROGRAM':
            self.match('PROGRAM')

            self.declarations()
            self.tree.add_child(self.declarationList)

            self.match('BEGIN')

            statementList = Statements('<statements>')
            self.statement_sequence(statementList)
            self.tree.add_child(statementList)

            self.match('END')

    def declarations(self):
        if self.tokens[self.look_ahead] == 'VAR':
            self.match('VAR')

            ident_token = self.token_objects[self.look_ahead]  # ident(..) Token object (rm)
            self.match('ident')

            self.match('AS')

            type_token = self.type()  # Get Type Token object

            variable = Variable(ident_token, type_token)  # Create Variable
            self.declarationList.add_child(variable)  # Add Variable to Declaration Block
            self.variable_map[variable.name] = variable  # Map to be used for type checking

            self.match('SC')
            self.declarations()
        else:
            return

    def type(self):
        if self.tokens[self.look_ahead] == 'INT':
            self.match('INT')
            return self.token_objects[self.look_ahead - 1]
        elif self.tokens[self.look_ahead] == 'BOOL':
            self.match('BOOL')
            return self.token_objects[self.look_ahead - 1]

    def statement_sequence(self, statementList):
        if self.tokens[self.look_ahead].startswith('ident') or self.tokens[self.look_ahead] == 'IF' or \
                        self.tokens[self.look_ahead] == 'WHILE' or self.tokens[self.look_ahead] == 'WRITEINT':
            statement = self.statement()  # It will get a statement node (rm)
            statementList.add_child(statement)  # Adding node to statementList
            self.match('SC')
            self.statement_sequence(statementList)  # sending the parent to which all statement nodes are added
        else:
            return

    def statement(self):  # returns a statement node (rm)
        if self.tokens[self.look_ahead].startswith('ident'):
            return self.assignment()
        elif self.tokens[self.look_ahead] == 'IF':
            return self.if_statement()
        elif self.tokens[self.look_ahead] == 'WHILE':
            return self.while_statement()
        elif self.tokens[self.look_ahead] == 'WRITEINT':
            return self.writeint()

    def assignment(self):  # returns assignment node

        if self.tokens[self.look_ahead].startswith('ident'):
            ident_token = self.token_objects[self.look_ahead]
            self.match('ident')
            try:
                variable = self.variable_map[ident_token.value]  # get variable to assign from from variable map
                assign_token = self.token_objects[self.look_ahead]
                assign_token.value = ':='
                self.match('ASGN')
                if self.tokens[self.look_ahead] == 'READINT':

                    assign = AssignOp(variable, assign_token,
                                      ReadInt())  # AssignOp node = vaiablenode, assigntoken, readintnode
                    if variable.type != 'int':
                        assign.color = 'indianred1'
                        print('TypeError: {} is of {} type, cannot store {} type.'.format(variable.name, variable.type,
                                                                                          'int'))
                    self.match('READINT')
                    return assign
                else:
                    rhsnode = self.expression()
                    # variable.value = rhsnode.value : TO BE DONE IN INTERPRETER R.M.

                    assign = AssignOp(variable, assign_token, rhsnode)  # if RHS of assignOp is an expression
                    if variable.type != rhsnode.type:
                        assign.color = 'indianred1'
                        print('TypeError: {} is of {} type, cannot store {} type.'.format(variable.name, variable.type,
                                                                                          rhsnode.type))
                    return assign
            except KeyError:
                print(ident_token.value, ': Not Declared, Declare Before Assigning!')
                sys.exit(0)

    def if_statement(self):  # returns ifStatement node
        if self.tokens[self.look_ahead] == 'IF':
            self.match('IF')
            compareOp = self.expression()
            self.match('THEN')

            ifStatementList = Statements('<if_statements>')
            self.statement_sequence(ifStatementList)  # add to ifStatementList

            elseStatementList = self.else_clause()  # None if empty

            self.match('END')
            ifOp = IfOp(compareOp, ifStatementList, elseStatementList)
            return ifOp

    def else_clause(self):
        if self.tokens[self.look_ahead] == 'ELSE':
            self.match('ELSE')
            elseBlock = Statements('<else_statements>')
            self.statement_sequence(elseBlock)  # add to elseBlock
            return elseBlock
        else:
            return

    def while_statement(self):
        if self.tokens[self.look_ahead] == 'WHILE':
            self.match('WHILE')
            boolOp = self.expression()
            self.match('DO')

            whileBlock = Statements('<while_statements>')
            self.statement_sequence(whileBlock)  # add to whileBlock

            self.match('END')

            whileOp = WhileOp(boolOp, whileBlock)
            return whileOp

    def writeint(self):
        if self.tokens[self.look_ahead] == 'WRITEINT':
            self.match('WRITEINT')
            node = self.expression()
            writeint = WriteInt(node)
            return writeint

    def expression(self):
        if self.tokens[self.look_ahead].startswith('ident') or self.tokens[self.look_ahead].startswith(
                'num') or self.tokens[self.look_ahead].startswith('boollit') or self.tokens[self.look_ahead] == 'LP':

            node = self.simple_expression()
            if self.tokens[self.look_ahead].startswith('COMPARE'):
                compare_token = self.token_objects[self.look_ahead]
                self.match('COMPARE')
                rhs = self.expression()
                node2 = CompareOp(node, compare_token, rhs)  # returns a CompareOp
                if node.type != rhs.type:
                    node2.color = 'indianred1'
                    print('TypeError: Cannot compare {} type and {} type, Expected both int types.'.format(node.type,
                                                                                                           rhs.type))
                return node2
            return node

    def simple_expression(self):
        if self.tokens[self.look_ahead].startswith('ident') or self.tokens[self.look_ahead].startswith(
                'num') or self.tokens[self.look_ahead].startswith('boollit') or self.tokens[self.look_ahead] == 'LP':
            node = self.term()  # Gets a Variable|Num|Bool|MultiplicationOp
            if self.tokens[self.look_ahead].startswith('ADDITIVE'):
                additive_token = self.token_objects[self.look_ahead]
                self.match('ADDITIVE')
                rhs = self.simple_expression()
                node2 = BinOp(node, additive_token, rhs)  # AdditiveBinaryOp
                if node.type != rhs.type:
                    node2.color = 'indianred1'
                    print(
                        'TypeError: Cannot perform integer operations over {} and {}, Expected both int types.'.format(
                            node.type,
                            rhs.type))
                return node2
            return node

    def term(self):
        if self.tokens[self.look_ahead].startswith('ident') or self.tokens[self.look_ahead].startswith(
                'num') or self.tokens[self.look_ahead].startswith('boollit') or self.tokens[self.look_ahead] == 'LP':
            node = self.factor()  # Gets a Variable|Num|Bool|ParenthesisOp (rm)
            if self.tokens[self.look_ahead].startswith('MULTIPLICATIVE'):
                multiplicative_token = self.token_objects[self.look_ahead]
                self.match('MULTIPLICATIVE')
                rhs = self.term()
                node2 = BinOp(node, multiplicative_token, rhs)  # MulBinaryOp with id as node.op= op_string (rm)
                if node.type != rhs.type:
                    node2.color = 'indianred1'
                    print(
                        'TypeError: Cannot perform integer operations over {} and {}, Expected both int types.'.format(
                            node.type,
                            rhs.type))
                return node2
            return node

    def factor(self):
        if self.tokens[self.look_ahead].startswith('ident'):
            ident_token = self.token_objects[self.look_ahead]
            self.match('ident')
            return self.variable_map[ident_token.value]  # returns variable object

        elif self.tokens[self.look_ahead].startswith('num'):
            num_token = self.token_objects[self.look_ahead]
            self.match('num')
            return Num(num_token)  # returns num object

        elif self.tokens[self.look_ahead].startswith('boollit'):
            bool_token = self.token_objects[self.look_ahead]
            self.match('boollit')
            return Bool(bool_token)  # returns a bool object

        elif self.tokens[self.look_ahead] == 'LP':
            self.match('LP')
            node = self.simple_expression()  # returns and expression of objects (rm)
            self.match('RP')
            return node


if __name__ == '__main__':
    scanner = Scanner()
    parser = Parser(scanner)
    parser.parse()
