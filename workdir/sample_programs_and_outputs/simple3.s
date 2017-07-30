	.data
newline:	.asciiz "\n"
	.text
	.globl main
main:
	li $fp, 0x7ffffffc
B1:
	li $t0, 0
	sw $t0, 0($fp)
	li $v0, 5
	syscall
	add $t0, $v0, $zero
	sw $t0, 0($fp)
	j B2
B2:
	lw $t1, 0($fp)
	li $t2, 0
	sw $t2, -8($fp)
	lw $t3, -8($fp)
	add $t2, $t3, $zero
	sgt $t0, $t1, $t2
	sw $t0, -4($fp)
	lw $t2, -4($fp)
	bne $t2, $zero, B3
L4:
	j B4
B3:
	j B5
B5:
	lw $t1, 0($fp)
	li $t2, 2
	sw $t2, -20($fp)
	lw $t3, -20($fp)
	add $t2, $t3, $zero
	rem $t0, $t1, $t2
	sw $t0, -16($fp)
	lw $t2, -16($fp)
	add $t1, $t2, $zero
	li $t3, 0
	sw $t3, -24($fp)
	lw $t4, -24($fp)
	add $t3, $t4, $zero
	seq $t0, $t1, $t3
	sw $t0, -12($fp)
	lw $t3, -12($fp)
	bne $t3, $zero, B6
L7:
	j B7
B6:
	li $v0, 1
	li $t1, 1
	sw $t1, -28($fp)
	lw $t1, -28($fp)
	add $a0, $t1, $zero
	syscall
	li $v0, 4
	la $a0, newline
	syscall
	j B8
B7:
	li $v0, 1
	li $t1, 0
	sw $t1, -32($fp)
	lw $t1, -32($fp)
	add $a0, $t1, $zero
	syscall
	li $v0, 4
	la $a0, newline
	syscall
B8:

B4:
	j B9
B9:
	li $v0, 10
	syscall