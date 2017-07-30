import textwrap
import sys
import re
from scanner import Scanner
from astparsing import Parser
from ast_visual import NodeVisitor, ASTVisualizer
from asmgeneration import AssemblyGenerator
from subprocess import check_output

scanner = Scanner()
parser = Parser(scanner)  # ast parser rm

visualize = ASTVisualizer(parser)  # create ASTVisualizer object
visualize.gendot()  # get the content of dot file ro

parser = Parser(scanner)  # ast parser rm
asm = AssemblyGenerator(parser)  # ASM GEN OBJECT
_ = asm.gens()  # get the content of .s file ro

content = ''.join(asm.dot_body)
# print(content)

cfg_header = [textwrap.dedent("""\
                digraph astgraph {
                  node [shape=box, style = filled, fillcolor=\"white\", fontsize=10, fontname="Courier", height=.09];
                  ranksep=.3;
                  edge [arrowsize=.5]
                """)]

cfg_footer = ['}']

cfg_body = []

# All Jump Statements Collected
jumps = []
for b in asm.dot_body:
    b = b.strip()
    if b.startswith('j '):
        jumps.append(b)
        # print(b)

block_pattern = r'B[0-9]+?:'
blocks = re.findall(block_pattern, content)
# print(blocks)
# All block names collected
block_dict = {}
for b in blocks:
    block_dict[b] = []

# All block bodies collected
for line in asm.dot_body:
    if line.startswith('B'):
        name = line.strip()
    line = re.sub('\t', '', line)
    block_dict[name].append(line)

keys = block_dict.keys()
keys = sorted(keys)

s = '  node{} [label="{}"]\n'.format(0, 'ENTER')
cfg_body.append(s)
s = '  node{} -> node{}\n'.format(0, 1)
cfg_body.append(s)

for idx, k in enumerate(keys):
    child = -1

    v = block_dict[k]
    number = k[1:-1]

    label = ''.join(v)
    # THIS BLOCK
    s = '  node{} [label="{}"]\n'.format(number, label)
    cfg_body.append(s)

    # SUCCESSOR
    try:
        child = keys[idx + 1][1]
        s = '  node{} -> node{}\n'.format(number, child)
        cfg_body.append(s)

    except IndexError:
        child = -1
        pass

    for j in set(jumps):
        if j in label:
            child_num = j.strip()[3:]
            if child != child_num:
                s = '  node{} -> node{}\n'.format(number, child_num)
                cfg_body.append(s)

content = ''.join(cfg_header + cfg_body + cfg_footer)
dot_file = asm.parser.scanner.opfilename[:-3] + 'cfg.dot'
jpg_file = asm.parser.scanner.opfilename[:-3] + 'cfg.jpg'
with open(dot_file, 'w') as file:
    file.write(content)
    print('CFG Dot file Generated Successfully.')

try:
    op = check_output(['dot', '-Tjpg', dot_file, '-o', jpg_file])

    print('CFG JPG Rendered Successfully.')
except FileNotFoundError:
    print(
        'Ignore this Error or | sudo apt-get install graphviz | for rendering Abstract Syntax Tree(.jpg), totally optional!!')
    print('AST Dot file Generated Successfully.')
