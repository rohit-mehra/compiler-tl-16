## Run Command

chmod +x exec.sh
./exec.sh <filepath to basename.tl>

## Example Run Synopsis

./exec.sh simple1.tl

**Generates:**

- simple1.tok ----------> file containing List of tokens or Error
- simple1.ast.dot ------> graphviz dot file containing AST (type checked)
- simple1.ast.jpg ------> jpg render of Abstract Syntax Tree dot file (type checked, with red nodes as error)
- simple1.cfg.dot ------> graphviz dot file containing CFG
- simple1.cfg.jpg ------> jpg render of Control Flow Graph dot file
- simple1.s ------------> string representation of the MIPS code

## TOUBLESHOOT

If some error persists, try:

python3 ./../main.py <basename.tl>

## More Example Runs

[TL 16.0 programs and their compiled outputs](sample_programs_and_outputs)
