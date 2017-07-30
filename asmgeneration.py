"""To GENERATE ASM"""
import textwrap
import sys
from scanner import Scanner
from astparsing import Parser
from ast_visual import NodeVisitor, ASTVisualizer
from subprocess import check_output

__author__ = 'rohitmehra'


class AssemblyGenerator(NodeVisitor):
    def __init__(self, ast_parser):
        self.parser = ast_parser
        self.parser.parse()
        self.variable_map = self.parser.variable_map
        self.fp_map = {}

        self.ncount = 1
        self.dot_header = [
            '\t.data\nnewline:\t.asciiz "\\n"\n\t.text\n\t.globl main\nmain:\n\tli $fp, 0x7ffffffc\n']
        self.dot_body = []
        # Starts from 4, updated to 0 before  use
        self.fp = 4
        # fp stack
        self.fp_Stack = []
        # block_stack
        self.block_stack = []

        self.t = 0
        self.v = 0
        self.a = 0
        self.block_count = 1

    def get_fp(self):
        return self.fp_Stack.pop()

    def get_block(self):
        return self.block_stack.pop()

    def del_second_last_block(self):
        del self.block_stack[-2]

    def update_t(self):
        if self.t <= 9:
            self.t += 1
        else:
            self.t = 0

    def load_Variable(self, node, t):
        name = node.name
        fp = self.variable_map[name].fp
        s = '\tlw $t{}, {}($fp)\n'.format(t, fp)
        self.dot_body.append(s)
        # self.fp_Stack.append(fp)

    # LOADS Number in current fp
    def visit_Num(self, node):
        # self.t = 0
        # UPDATE fp and then use.
        self.fp -= 4
        # s = '\tli $t{}, {}\n\tsw $t{}, {}($fp)\n\tlw $t{}, {}($fp)\n\tadd $t{}, $t{}, $zero\n'.format(self.t,
        #                                                                                               node.value,
        #                                                                                               self.t, self.fp,
        #                                                                                               self.t + 1,
        #                                                                                               self.fp,
        #                                                                                               self.t,
        #                                                                                               self.t + 1)
        s = '\tli $t{}, {}\n\tsw $t{}, {}($fp)\n'.format(self.t,
                                                         node.value,
                                                         self.t,
                                                         self.fp,
                                                         )
        self.fp_Stack.append(self.fp)
        self.dot_body.append(s)

    # LOADS Bool in current fp
    def visit_Bool(self, node):
        # self.t = 0
        # UPDATE fp and then use.
        self.fp -= 4

        if node.value == 'true':
            value = 1
        else:
            value = 0

        s = '\tli $t{}, {}\n\tsw $t{}, {}($fp)\n'.format(self.t,
                                                         value,
                                                         self.t,
                                                         self.fp,
                                                         )
        self.fp_Stack.append(self.fp)
        self.dot_body.append(s)

    # DECLARATIONS CALLS & VARIABLE MAP UPDATES
    def visit_Variable(self, node):
        # fp starts from 4        # fp indicates each unique variable
        # UPDATE fp and then use.
        self.fp -= 4
        s = '\tli $t{}, 0\n\tsw $t{}, {}($fp)\n'.format(
            self.t, self.t, self.fp)
        self.dot_body.append(s)

        self.variable_map[node.name].fp = self.fp

    def visit_ReadInt(self, node):
        # INPUT and MOVE to current t
        s = '\tli $v{}, 5\n\tsyscall\n\tadd $t{}, $v{}, $zero\n'.format(
            self.v, self.t, self.v)
        self.dot_body.append(s)
        # Returns back to calling block and there will be save word call

    # Type 1.2
    def visit_WriteInt(self, node):
        self.t = 0
        s = '\tli $v{}, 1\n'.format(self.v)
        self.dot_body.append(s)
        self.update_t()
        current_t = self.t

        if type(node.child).__name__ == 'Variable':
            self.load_Variable(node.child, current_t)
        else:
            self.visit(node.child)
            s = '\tlw $t{}, {}($fp)\n'.format(current_t, self.get_fp())
            self.dot_body.append(s)

        s = '\tadd $a{}, $t{}, $zero\n\tsyscall\n\tli $v{}, 4\n\tla $a{}, newline\n\tsyscall\n'.format(self.a, self.t,
                                                                                                       self.v, self.a)
        self.dot_body.append(s)

    # ASSIGNMENTS
    def visit_AssignOp(self, node):
        # Temp register to be used
        self.t = 0
        # Get the variable name
        variable_name = node.left.name
        # Get the fp of that variable
        variable_fp = self.variable_map[variable_name].fp

        # Call Right Nodes First
        # ReadInt type assignments
        if type(node.right).__name__ == 'ReadInt':
            # Will load word from user to self.t
            self.visit(node.right)

        # Just Single Variable onto right
        elif type(node.right).__name__ == 'Variable':
            # Load right Variable to self.t
            self.load_Variable(node.right, self.t)

        # Either Bool or Num or BinaryOp or CompareOp
        else:
            self.visit(node.right)
            # LOAD RHS FROM ITS fp to t+1, move to t and then to LHS variable FP
            s = '\tlw $t{}, {}($fp)\n\tadd $t{}, $t{}, $zero\n'.format(self.t + 1,
                                                                       self.get_fp(),
                                                                       self.t,
                                                                       self.t + 1)
            self.dot_body.append(s)

        # Store word to the LHS variable fp
        s = '\tsw $t{}, {}($fp)\n'.format(self.t, variable_fp)
        self.dot_body.append(s)

    # Make Call for all ops then save the result in current fp
    def visit_BinOp(self, node):
        self.t = 0
        self.fp -= 4  # fp of this op
        # pushed into stack, Popped at receiving end
        self.fp_Stack.append(self.fp)

        current_t = self.t  # t for this op

        self.update_t()
        left = self.t  # t holding left operand

        if type(node.left).__name__ == 'Variable':
            # load variable from fp to left t
            self.load_Variable(node.left, left)
        else:
            # Either Bool or Num or BinaryOp or CompareOp
            self.visit(node.left)
            s = '\tlw $t{}, {}($fp)\n\tadd $t{}, $t{}, $zero\n'.format(left + 1,
                                                                       self.get_fp(),
                                                                       left,
                                                                       left + 1)
            self.dot_body.append(s)

        self.update_t()
        right = self.t  # t holding right operand

        if type(node.right).__name__ == 'Variable':
            # load variable from fp to right t
            self.load_Variable(node.right, right)

        else:
            # Either Bool or Num or BinaryOp or CompareOp
            self.visit(node.right)
            s = '\tlw $t{}, {}($fp)\n\tadd $t{}, $t{}, $zero\n'.format(right + 1,
                                                                       self.get_fp(),
                                                                       right,
                                                                       right + 1)
            self.dot_body.append(s)

        if node.op.value == '+':
            s = '\tadd $t{}, $t{}, $t{}\n'.format(current_t, left, right)
            self.dot_body.append(s)
        elif node.op.value == '-':
            s = '\tsub $t{}, $t{}, $t{}\n'.format(current_t, left, right)
            self.dot_body.append(s)
        elif node.op.value == '*':
            s = '\tmul $t{}, $t{}, $t{}\n'.format(current_t, left, right)
            self.dot_body.append(s)
        elif node.op.value == 'div':
            s = '\tdiv $t{}, $t{}, $t{}\n'.format(current_t, left, right)
            self.dot_body.append(s)
        elif node.op.value == 'mod':
            s = '\trem $t{}, $t{}, $t{}\n'.format(current_t, left, right)
            self.dot_body.append(s)

        # Store word at fp(read from stack) of this op, will be popped at the receiver end
        s = '\tsw $t{}, {}($fp)\n'.format(current_t, self.fp_Stack[-1])
        self.dot_body.append(s)

    def visit_CompareOp(self, node):
        self.t = 0
        self.fp -= 4  # fp of this op
        # pushed into stack, Popped at receiving end
        self.fp_Stack.append(self.fp)

        current_t = self.t  # t for this op

        self.update_t()
        left = self.t  # t holding left operand

        if type(node.left).__name__ == 'Variable':
            # load variable from fp to left t
            self.load_Variable(node.left, left)

        else:
            # Either Bool or Num or BinaryOp or CompareOp
            self.visit(node.left)
            s = '\tlw $t{}, {}($fp)\n\tadd $t{}, $t{}, $zero\n'.format(left + 1,
                                                                       self.get_fp(),
                                                                       left,
                                                                       left + 1)
            self.dot_body.append(s)

        self.update_t()
        right = self.t  # t holding right operand

        if type(node.right).__name__ == 'Variable':
            # load variable from fp to right t
            self.load_Variable(node.right, right)

        else:
            # Either Bool or Num or BinaryOp or CompareOp
            self.visit(node.right)
            s = '\tlw $t{}, {}($fp)\n\tadd $t{}, $t{}, $zero\n'.format(right + 1,
                                                                       self.get_fp(),
                                                                       right,
                                                                       right + 1)
            self.dot_body.append(s)

        if node.op.value == '<':
            s = '\tslt $t{}, $t{}, $t{}\n'.format(current_t, left, right)
            self.dot_body.append(s)
        elif node.op.value == '<=':
            s = '\tsle $t{}, $t{}, $t{}\n'.format(current_t, left, right)
            self.dot_body.append(s)
        elif node.op.value == '>':
            s = '\tsgt $t{}, $t{}, $t{}\n'.format(current_t, left, right)
            self.dot_body.append(s)
        elif node.op.value == '>=':
            s = '\tsge $t{}, $t{}, $t{}\n'.format(current_t, left, right)
            self.dot_body.append(s)
        elif node.op.value == '!=':
            s = '\tsne $t{}, $t{}, $t{}\n'.format(current_t, left, right)
            self.dot_body.append(s)
        elif node.op.value == '=':
            s = '\tseq $t{}, $t{}, $t{}\n'.format(current_t, left, right)
            self.dot_body.append(s)

        # Store word at fp(read from stack) of this op, will be popped at the receiver end
        s = '\tsw $t{}, {}($fp)\n'.format(current_t, self.fp_Stack[-1])
        self.dot_body.append(s)

    # Type 3
    def visit_WhileOp(self, node):

        self.block_count += 1
        # adding statement block and exit block to stack
        current_block = self.block_count

        self.block_stack.extend([self.block_count + 1, self.block_count + 2])
        self.block_count += 2

        self.t = 0
        # Jump from previous block to this block
        s = '\tj B{}\n'.format(current_block)
        self.dot_body.append(s)

        # 1) CONDITIONAL BLOCK
        s = 'B{}:\n'.format(current_block)
        self.dot_body.append(s)

        # Comparision node, execute comparision-->store result in fp--> push to fp stack
        self.visit(node.comparision)

        # Pop fp_stack and load from fp to current t
        s = '\tlw $t{}, {}($fp)\n'.format(self.t, self.get_fp())
        self.dot_body.append(s)

        # If not 0/false jump to while  block, create a label used to exit while loop/jump to next block.
        exit_block = self.get_block()
        while_block = self.get_block()

        s = '\tbne $t{}, $zero, B{}\n'.format(self.t, while_block)
        self.dot_body.append(s)

        s = 'L{}:\n'.format(current_block)
        self.dot_body.append(s)

        s = '\tj B{}\n'.format(exit_block)
        self.dot_body.append(s)

        s = 'B{}:\n'.format(while_block)
        self.dot_body.append(s)

        # 2) WHILE STATEMENTS BLOCK
        self.visit(node.statements)

        # 3) LOOP BACK TO CONDITIONAL BLOCK
        s = '\tj B{}\n'.format(current_block)
        self.dot_body.append(s)

        s = 'B{}:\n'.format(exit_block)
        self.dot_body.append(s)

    # Type 4
    def visit_IfOp(self, node):

        self.block_count += 1
        self.block_stack.append(self.block_count)

        # adding statement block and exit block to stack
        current_block = self.get_block()  # condition block

        self.t = 0
        # Jump from previous block to this block
        s = '\tj B{}\n'.format(current_block)
        self.dot_body.append(s)

        # 1) CONDITIONAL BLOCK
        s = 'B{}:\n'.format(current_block)
        self.dot_body.append(s)

        # Comparision node, execute comparision-->store result in fp--> push to fp stack
        # node.comparison could be a compareOp or a bool variable
        if type(node.comparision).__name__ == 'Variable':
            self.load_Variable(node.comparision, self.t)

        else:
            self.visit(node.comparision)
            # Pop fp_stack and load from fp to current t
            s = '\tlw $t{}, {}($fp)\n'.format(self.t, self.get_fp())
            self.dot_body.append(s)

        # If not 0/false jump to if  block
        self.block_count += 1  # If block count
        if_block = self.block_count
        self.block_stack.append(self.block_count)

        s = '\tbne $t{}, $zero, B{}\n'.format(self.t, self.block_count)
        self.dot_body.append(s)

        ######################################
        # Create label for else statements

        self.block_count += 1  # Else block count
        # ADDED, WILL BE POPPED OR REMAIN IN STACK
        self.block_stack.append(self.block_count)

        s = 'L{}:\n'.format(self.block_count)
        self.dot_body.append(s)

        s = '\tj B{}\n'.format(self.block_count)
        self.dot_body.append(s)

        # 2) IF STATEMENTS BLOCK

        s = 'B{}:\n'.format(if_block)
        self.dot_body.append(s)

        self.visit(node.if_statements)  # --------------->

        # 3) if else statement exist, then call else statements in the block in label
        if node.else_statements:
            # POP ELSE BLOCK| WONT BE POPPED WILL REMAIN IN THE STACK TILL END
            exit_block = self.get_block()
            _ = self.get_block()  # POP IF BLOCK
            s = '\tj B{}\n'.format(exit_block + 1)
            self.dot_body.append(s)

            s = 'B{}:\n'.format(exit_block)
            self.dot_body.append(s)
            # Append else clause to this block
            self.visit(node.else_statements)  # --------------->
            self.block_count += 1
            s = 'B{}:\n'.format(self.block_count)
            self.dot_body.append(s)

        if not node.else_statements:
            self.del_second_last_block()
            s = '\nB{}:\n'.format(self.get_block())
            self.dot_body.append(s)

    # Assignments followed by main body
    def visit_Statements(self, node):
        # Add Statements to the same block it was invoked from
        for child in node.children:
            self.t = 0
            self.visit(child)

    # DONE
    def visit_Declarations(self, node):
        # Add Declarations to the same block it was invoked from
        for child in node.children:
            self.visit(child)

    # DONE
    def visit_Program(self, node):
        # First Block
        s = 'B{}:\n'.format(self.block_count)
        self.dot_body.append(s)

        # Add statements to the first block
        for child in node.children:
            self.visit(child)

        # EXIT CALL
        self.block_count += 1
        s = '\tj B{}\n'.format(self.block_count)
        self.dot_body.append(s)

        s = 'B{}:\n'.format(self.block_count)
        self.dot_body.append(s)

        s = '\tli $v{}, 10\n\tsyscall'.format(self.v)
        self.dot_body.append(s)
        # print(self.block_stack, len(self.block_stack))

    def gens(self):
        self.visit(self.parser.tree)

        content = ''.join(self.dot_header + self.dot_body)
        s_file = self.parser.scanner.opfilename[:-3] + 's'
        with open(s_file, 'w') as file:
            file.write(content)
        print('Compiled .s file Generated Successfully.')

        return content


if __name__ == '__main__':
    scanner = Scanner()
    parser = Parser(scanner)  # ast parser rm

    visualize = ASTVisualizer(parser)  # create ASTVisualizer object
    visualize.gendot()  # get the content of dot file ro

    parser = Parser(scanner)  # ast parser rm
    asm = AssemblyGenerator(parser)  # ASM GEN OBJECT
    content = asm.gens()  # get the content of .s file ro
