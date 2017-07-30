	.data
newline:	.asciiz "\n"
	.text
	.globl main
main:
	li $fp, 0x7ffffffc
B1:
	li $t0, 0
	sw $t0, 0($fp)
	li $t0, 0
	sw $t0, -4($fp)
	li $t0, 0
	sw $t0, -8($fp)
	li $t0, 0
	sw $t0, -12($fp)
	li $v0, 5
	syscall
	add $t0, $v0, $zero
	sw $t0, 0($fp)
	li $t0, 2
	sw $t0, -16($fp)
	lw $t1, -16($fp)
	add $t0, $t1, $zero
	sw $t0, -4($fp)
	li $t0, 1
	sw $t0, -20($fp)
	lw $t1, -20($fp)
	add $t0, $t1, $zero
	sw $t0, -12($fp)
	j B2
B2:
	lw $t1, -4($fp)
	lw $t2, 0($fp)
	slt $t0, $t1, $t2
	sw $t0, -24($fp)
	lw $t2, -24($fp)
	bne $t2, $zero, B3
L2:
	j B4
B3:
	lw $t1, 0($fp)
	lw $t2, -4($fp)
	rem $t0, $t1, $t2
	sw $t0, -28($fp)
	lw $t3, -28($fp)
	add $t2, $t3, $zero
	sw $t2, -8($fp)
	j B5
B5:
	lw $t1, -8($fp)
	li $t2, 0
	sw $t2, -36($fp)
	lw $t3, -36($fp)
	add $t2, $t3, $zero
	seq $t0, $t1, $t2
	sw $t0, -32($fp)
	lw $t2, -32($fp)
	bne $t2, $zero, B6
L7:
	j B7
B6:
	li $t0, 0
	sw $t0, -40($fp)
	lw $t1, -40($fp)
	add $t0, $t1, $zero
	sw $t0, -12($fp)

B7:
	lw $t1, -4($fp)
	li $t2, 1
	sw $t2, -48($fp)
	lw $t3, -48($fp)
	add $t2, $t3, $zero
	add $t0, $t1, $t2
	sw $t0, -44($fp)
	lw $t3, -44($fp)
	add $t2, $t3, $zero
	sw $t2, -4($fp)
	j B2
B4:
	j B8
B8:
	li $v0, 10
	syscall