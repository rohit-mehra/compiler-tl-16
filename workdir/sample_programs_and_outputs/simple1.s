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
	li $v0, 5
	syscall
	add $t0, $v0, $zero
	sw $t0, 0($fp)
	li $t0, 0
	sw $t0, -8($fp)
	lw $t1, -8($fp)
	add $t0, $t1, $zero
	sw $t0, -4($fp)
	j B2
B2:
	lw $t1, -4($fp)
	lw $t2, -4($fp)
	mul $t0, $t1, $t2
	sw $t0, -16($fp)
	lw $t2, -16($fp)
	add $t1, $t2, $zero
	lw $t3, 0($fp)
	sle $t0, $t1, $t3
	sw $t0, -12($fp)
	lw $t3, -12($fp)
	bne $t3, $zero, B3
L2:
	j B4
B3:
	lw $t1, -4($fp)
	li $t2, 1
	sw $t2, -24($fp)
	lw $t3, -24($fp)
	add $t2, $t3, $zero
	add $t0, $t1, $t2
	sw $t0, -20($fp)
	lw $t3, -20($fp)
	add $t2, $t3, $zero
	sw $t2, -4($fp)
	j B2
B4:
	lw $t1, -4($fp)
	li $t2, 1
	sw $t2, -32($fp)
	lw $t3, -32($fp)
	add $t2, $t3, $zero
	sub $t0, $t1, $t2
	sw $t0, -28($fp)
	lw $t3, -28($fp)
	add $t2, $t3, $zero
	sw $t2, -4($fp)
	li $v0, 1
	lw $t1, -4($fp)
	add $a0, $t1, $zero
	syscall
	li $v0, 4
	la $a0, newline
	syscall
	j B5
B5:
	li $v0, 10
	syscall