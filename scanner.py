#!/usr/bin/env python3
import re
import sys
from pyparsing import OneOrMore, ZeroOrMore, Regex, Keyword, Forward  # Used just for pre checking of grammar | Optional

__author__ = 'rohitmehra'
keywords = {'if', 'then', 'else', 'begin', 'end', 'while', 'do', 'program', 'var', 'as', 'int', 'bool',
            'writeInt',
            'readInt', 'div', 'mod', 'true', 'false'}
MULTIPLICATIVE = {'div', 'mod'}
boollit = {'true', 'false'}

token_specification = [
    ('num', r'[1-9][0-9]*|0'),  # Integer or decimal number rm
    ('ASGN', r':='),  # Assignment operator
    ('LP', r'\('),  # LP
    ('RP', r'\)'),  # RP
    ('SC', r';'),  # Statement terminator rm
    ('ident', r'[a-z_A-Z][a-zA-Z0-9]*'),  # Identifiers
    ('MULTIPLICATIVE', r'[*]'),  # Arithmetic operators
    ('COMPARE', r'[<][=]|[>][=]|[!][=]|[<]|[>]|[=]'),  # Comparatives (rm)
    ('ADDITIVE', r'[+\-]'),  # Additive Operators
    ('NEWLINE', r'\n'),  # Line endings rm
    ('SKIP', r'[ \t]+|%.*'),  # Skip over spaces and tabs
    ('MISMATCH', r'.'),  # Any other character
]


class Token:
    def __init__(self, typ, value):
        self.type = typ
        self.value = value

    def __str__(self):
        """String representation of the Token instance.RM"""
        if self.value:
            return '{type}({value})'.format(
                type=self.type,
                value=self.value
            )
        else:
            return self.type

    def __repr__(self):
        return self.__str__()


class Scanner:
    def __init__(self, progam='%'):
        self.tokens = []
        self.token_objects = []
        self.opfilename = 'test.tok'
        self.program = progam
        self.input(progam)

    @staticmethod
    def tokenize(code_file_string):
        all_patterns = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        line_num = 1
        for match_object in re.finditer(all_patterns, code_file_string):

            kind = match_object.lastgroup  # matches the first group in the line that is matched
            value = match_object.group(kind)

            if kind == 'NEWLINE':
                line_num += 1
            elif kind == 'SKIP':
                pass
            elif kind == 'MISMATCH' or (kind == 'num' and abs(int(value)) > 2147483647):
                # raise RuntimeError('SCANNER ERROR: %r unexpected on line %d' % (value, line_num))
                yield Token('SCANNER ERROR: %r unexpected on line %d' % (value, line_num), None)
            else:
                if kind == 'ident' and (value in keywords):
                    if value in MULTIPLICATIVE:
                        kind = 'MULTIPLICATIVE' + '(' + value + ')'
                    elif value in boollit:
                        kind = 'boollit' + '(' + value + ')'
                    else:
                        kind = value.upper()
                if kind == value.upper() or (kind in ['LP', 'RP', 'ASGN', 'SC']) or (value in keywords):
                    tok = kind  # For Keywords
                else:
                    tok = kind + '(' + value + ')'  # for XYZ(SYMBOLS)
                # Into token Object rm
                if '(' in tok:
                    token = Token(tok[:tok.index('(')], value)
                    yield token
                elif '(' not in tok:
                    token = Token(kind, None)
                    yield token

    @staticmethod
    def grammar_check(token_string):  # pre checking grammar with help of external module | Optional
        start, end = Keyword('PROGRAM'), Keyword('END')
        intg, boole = Keyword('INT'), Keyword('BOOL')
        lp, rp = Keyword('LP'), Keyword('RP')
        sc = Keyword('SC')
        ident = Regex(r'ident\(.+?\)')
        num = Regex(r'num\(.+?\)')
        compare = Regex(r'COMPARE\(.+?\)')
        additive = Regex(r'ADDITIVE\(.+?\)')
        multi = Regex(r'MULTIPLICATIVE\(.+?\)')
        boollit = Regex(r'boollit\(.+?\)')
        typ = intg ^ boole
        expression = Forward()
        statementSequence = Forward()

        factor = ident ^ num ^ boollit ^ (lp + expression + rp)
        term = (OneOrMore(factor + multi) + factor) ^ factor
        simpleExpression = (OneOrMore(term + additive) + term) ^ term
        expression <<= (OneOrMore(simpleExpression + compare) + simpleExpression) ^ simpleExpression

        elseClause = ZeroOrMore('ELSE' + statementSequence)
        ifStatement = 'IF' + expression + 'THEN' + statementSequence + elseClause + end
        whileStatement = 'WHILE' + expression + 'DO' + statementSequence + end

        assignment = ((ident + 'ASGN' + expression) ^ (ident + 'ASGN' + 'READINT'))
        writeInt = 'WRITEINT' + expression
        statement = (assignment ^ ifStatement ^ whileStatement ^ writeInt)
        statementSequence <<= ZeroOrMore(statement + sc)
        declarations = ZeroOrMore('VAR' + ident + 'AS' + typ + sc)
        program = start + declarations + 'BEGIN' + statementSequence + end
        try:
            program.parseString(token_string)
            return True
        except:
            return False

    def input(self, prog='%'):
        if prog == '%':
            try:
                with open(sys.argv[1], 'r') as string:
                    if str(sys.argv[1])[-3:] != '.tl':
                        raise RuntimeError('Only .tl Files can be Parsed!!')
                    self.file = string.read()
                    self.opfilename = str(sys.argv[1][:-2]) + 'tok'
            except UnicodeDecodeError:
                with open(sys.argv[1], 'r', encoding='latin1') as string:
                    self.file = string.read()
                    self.opfilename = str(sys.argv[1][:-2]) + 'tok'
            except Exception as e:
                print('FileNotFound: %s' % e)
                sys.exit(2)
            self.program = self.file

    def parse(self):
        token_error = False
        for token in self.tokenize(self.program):
            if token.__repr__().startswith('SCANNER ERROR'):
                token_error = token.__repr__()
            else:
                self.tokens.append(token.__repr__())
                self.token_objects.append(token)

        if token_error:
            with open(self.opfilename, 'w') as file:
                file.write(token_error)
            print(token_error)
            sys.exit(0)
        else:
            token_stream = '\n'.join(self.tokens)
            if not self.grammar_check(token_stream):
                with open(self.opfilename, 'w') as file:
                    file.write('SYNTAX ERROR')
                print('SYNTAX ERROR')
            else:
                with open(self.opfilename, 'w') as file:
                    file.writelines(token_stream)


if __name__ == '__main__':
    prog = '''program
  var N as int ;
  var SQRT as int ;
begin
  N := readInt ;
  SQRT := 0 ;

  while SQRT * SQRT <= N do
    SQRT := SQRT + 1 ;
  end ;

  SQRT := SQRT - 1 ;

  writeInt SQRT ; %(rm)

end '''
    s = Scanner()  # object with input initialized
    s.parse()  # tokenize and update tokens and token_objects list of scanner object
