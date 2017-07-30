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
	sw $t0, -8($fp)
	li $t0, 1
	sw $t0, -16($fp)
	lw $t1, -16($fp)
	add $t0, $t1, $zero
	sw $t0, 0($fp)
	li $t0, 0
	sw $t0, -20($fp)
	lw $t1, -20($fp)
	add $t0, $t1, $zero
	sw $t0, -4($fp)
	li $t0, 1
	sw $t0, -24($fp)
	lw $t1, -24($fp)
	add $t0, $t1, $zero
	sw $t0, -12($fp)
	li $v0, 1
	li $t1, 0
	sw $t1, -28($fp)
	lw $t1, -28($fp)
	add $a0, $t1, $zero
	syscall
	li $v0, 4
	la $a0, newline
	syscall
	j B2
B2:
	lw $t1, -12($fp)
	lw $t2, -8($fp)
	sle $t0, $t1, $t2
	sw $t0, -32($fp)
	lw $t2, -32($fp)
	bne $t2, $zero, B3
L2:
	j B4
B3:
	li $v0, 1
	lw $t1, -12($fp)
	add $a0, $t1, $zero
	syscall
	li $v0, 4
	la $a0, newline
	syscall
	lw $t1, 0($fp)
	lw $t2, -4($fp)
	add $t0, $t1, $t2
	sw $t0, -36($fp)
	lw $t3, -36($fp)
	add $t2, $t3, $zero
	sw $t2, -12($fp)
	lw $t0, 0($fp)
	sw $t0, -4($fp)
	lw $t0, -12($fp)
	sw $t0, 0($fp)
	j B2
B4:
	j B5
B5:
	li $v0, 10
	syscall