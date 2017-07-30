## Synopsis

The project is to design and develop a compiler for the "Toy Language", described in TL 16.0 specifications, which is derived from a simplified subset of Pascal. The compiler translates TL source code, producing output at several intermediate stages, into MIPS assembly code executable in a simulator. We implemented this compiler using Python 3.5 language and PyCharm IDE.

## Code Example

#### Run Command

- cd workdir
- chmod +x exec.sh
- ./exec.sh <filepath to basename.tl>

#### Example Run Synopsis

./exec.sh simple1.tl

**Generates:**

- simple1.tok ----------> file containing List of tokens or Error
- simple1.ast.dot ------> graphviz dot file containing AST (type checked)
- simple1.ast.jpg ------> jpg render of Abstract Syntax Tree dot file (type checked, with red nodes as error)
- simple1.cfg.dot ------> graphviz dot file containing CFG
- simple1.cfg.jpg ------> jpg render of Control Flow Graph dot file
- simple1.s ------------> string representation of the MIPS code

#### TOUBLESHOOT

If some error persists, try:

python3 ./../main.py <basename.tl>

#### More Example Runs

[TL 16.0 programs and their compiled outputs](workdir/sample_programs_and_outputs)

## Motivation

The project is developed as part of the Programming Languages and Compilers Course during Spring 2017. Main idea behind this project was to provide us the experience of writing a compiler without getting burdened by all of the complexities and details of a complete, standard programming language.

## Requirements

- Python 3.5 - sudo apt-get install python3
- Graphviz - sudo apt-get install graphviz
- QT simulator

## License

MIT License

Copyright (c) [2017] [Rohit Mehra]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
