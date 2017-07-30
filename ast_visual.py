"""To Visualize the AST"""
import textwrap
from scanner import Scanner
from astparsing import Parser
from subprocess import check_output

__author__ = 'rohitmehra'


class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name,
                          self.generic_visit)  # get the named function if not exist return generic visit
        return visitor(node)  # return the func(node)

    @staticmethod
    def generic_visit(node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class ASTVisualizer(NodeVisitor):
    def __init__(self, ast_parser):
        self.parser = ast_parser
        self.ncount = 1
        self.dot_header = [textwrap.dedent("""\
                digraph astgraph {
                  node [shape=box, style = filled, fillcolor=\"white\", fontsize=10, fontname="Courier", height=.09];
                  ranksep=.3;
                  edge [arrowsize=.5]
                """)]
        self.dot_body = []
        self.dot_footer = ['}']

    # Type 1
    def visit_Num(self, node):
        s = '  node{} [label="{}"]\n'.format(self.ncount, node.__str__())
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

    def visit_Bool(self, node):
        s = '  node{} [label="{}"]\n'.format(self.ncount, node.__str__())
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

    def visit_Variable(self, node):
        s = '  node{} [label="{}"]\n'.format(self.ncount, node.__str__())
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

    def visit_ReadInt(self, node):
        s = '  node{} [label="{}"]\n'.format(self.ncount, node.__str__())
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

    # Type 1.2
    def visit_WriteInt(self, node):
        s = '  node{} [label="{}"]\n'.format(self.ncount, node.__str__())
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        self.visit(node.child)
        s = '  node{} -> node{}\n'.format(node._num, node.child._num)
        self.dot_body.append(s)

    # Type 2
    def visit_BinOp(self, node):
        s = '  node{} [label="{}", fillcolor="{}"]\n'.format(self.ncount, node.__str__(), node.color)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        self.visit(node.left)
        s = '  node{} -> node{}\n'.format(node._num, node.left._num)
        self.dot_body.append(s)

        self.visit(node.right)
        s = '  node{} -> node{}\n'.format(node._num, node.right._num)
        self.dot_body.append(s)

    def visit_AssignOp(self, node):
        s = '  node{} [label="{}", fillcolor="{}"]\n'.format(self.ncount, node.__str__(), node.color)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        self.visit(node.left)
        s = '  node{} -> node{}\n'.format(node._num, node.left._num)
        self.dot_body.append(s)

        self.visit(node.right)
        s = '  node{} -> node{}\n'.format(node._num, node.right._num)
        self.dot_body.append(s)

    def visit_CompareOp(self, node):
        s = '  node{} [label="{}", fillcolor="{}"]\n'.format(self.ncount, node.__str__(), node.color)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        self.visit(node.left)
        s = '  node{} -> node{}\n'.format(node._num, node.left._num)
        self.dot_body.append(s)

        self.visit(node.right)
        s = '  node{} -> node{}\n'.format(node._num, node.right._num)
        self.dot_body.append(s)

    # Type 3
    def visit_WhileOp(self, node):
        s = '  node{} [label="{}"]\n'.format(self.ncount, node.name)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        self.visit(node.comparision)
        s = '  node{} -> node{}\n'.format(node._num, node.comparision._num)
        self.dot_body.append(s)

        self.visit(node.statements)
        s = '  node{} -> node{}\n'.format(node._num, node.statements._num)
        self.dot_body.append(s)

    # Type 4
    def visit_IfOp(self, node):
        s = '  node{} [label="{}"]\n'.format(self.ncount, node.name)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        self.visit(node.comparision)
        s = '  node{} -> node{}\n'.format(node._num, node.comparision._num)
        self.dot_body.append(s)

        self.visit(node.if_statements)
        s = '  node{} -> node{}\n'.format(node._num, node.if_statements._num)
        self.dot_body.append(s)

        if node.else_statements:
            self.visit(node.else_statements)
            s = '  node{} -> node{}\n'.format(node._num, node.else_statements._num)
            self.dot_body.append(s)

    # Type 5
    def visit_Statements(self, node):
        s = '  node{} [label="{}"]\n'.format(self.ncount, node.name)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        for child in node.children:
            self.visit(child)
            s = '  node{} -> node{}\n'.format(node._num, child._num)
            self.dot_body.append(s)

    def visit_Declarations(self, node):
        s = '  node{} [label="{}"]\n'.format(self.ncount, node.name)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        for child in node.children:
            self.visit(child)
            s = '  node{} -> node{}\n'.format(node._num, child._num)
            self.dot_body.append(s)

    def visit_Program(self, node):
        s = '  node{} [label="{}"]\n'.format(self.ncount, node.name)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        for child in node.children:
            self.visit(child)
            s = '  node{} -> node{}\n'.format(node._num, child._num)
            self.dot_body.append(s)

    def gendot(self):
        self.parser.parse()
        self.visit(self.parser.tree)
        content = ''.join(self.dot_header + self.dot_body + self.dot_footer)

        dot_file = self.parser.scanner.opfilename[:-3] + 'ast.dot'
        jpg_file = self.parser.scanner.opfilename[:-3] + 'ast.jpg'
        with open(dot_file, 'w') as file:
            file.write(content)

        try:
            op = check_output(['dot', '-Tjpg', dot_file, '-o', jpg_file])
            print('AST Dot file Generated Successfully.')
            print('AST JPG Rendered Successfully.')
        except FileNotFoundError:
            print(
                'Ignore this Error or | sudo apt-get install graphviz | for rendering Abstract Syntax Tree(.jpg), totally optional!!')
            print('AST Dot file Generated Successfully.')


if __name__ == '__main__':
    scanner = Scanner()
    parser = Parser(scanner)  # ast parser rm
    visualize = ASTVisualizer(parser)  # create ASTVisualizer object
    visualize.gendot()  # get the content of dot file ro
