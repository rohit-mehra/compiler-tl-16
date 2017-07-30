import textwrap
from scanner import Scanner
from parsetreeparsing import Parser
from subprocess import check_output


class ParseTreeVisualizer:
    def __init__(self, parser):
        self.parser = parser
        self.ncount = 1
        self.dot_header = [textwrap.dedent("""\
        digraph astgraph {
          node [shape=box, style = filled, fillcolor=\"white\", fontsize=10, fontname="Courier", height=.09];
          ranksep=.3;
          edge [arrowsize=.5]
        """)]
        self.dot_body = []
        self.dot_footer = ['}']

    def bfs(self, node):
        ncount = 1
        queue = list()
        queue.append(node)
        s = '  node{} [label="{}"]\n'.format(ncount, node.name)
        self.dot_body.append(s)
        node._num = ncount
        ncount += 1

        while queue:
            node = queue.pop(0)
            for child_node in node.children:
                s = '  node{} [label="{}"]\n'.format(ncount, child_node.name)
                self.dot_body.append(s)
                child_node._num = ncount
                ncount += 1
                s = '  node{} -> node{}\n'.format(node._num, child_node._num)
                self.dot_body.append(s)
                queue.append(child_node)

    def gendot(self):
        self.parser.parse()
        tree = self.parser.tree
        self.bfs(tree)
        return ''.join(self.dot_header + self.dot_body + self.dot_footer)


if __name__ == '__main__':
    scanner = Scanner()
    parser = Parser(scanner)  # parse tree parser
    visualize = ParseTreeVisualizer(parser)
    content = visualize.gendot()

    dot_file = scanner.opfilename[:-3] + 'pt.dot'
    jpg_file = scanner.opfilename[:-3] + 'pt.jpg'
    with open(dot_file, 'w') as file:
        file.write(content)

    try:
        op = check_output(['dot', '-Tjpg', dot_file, '-o', jpg_file])
        print('Parse Tree Dot file Generated Successfully.')
        print('Parse tree JPG rendered.')
    except FileNotFoundError:
        print(
            'Ignore this Error or | sudo apt-get install graphviz | for rendering parse tree(.jpg), totally optional!!')
        print('Parse Tree Dot file Generated Successfully.')
