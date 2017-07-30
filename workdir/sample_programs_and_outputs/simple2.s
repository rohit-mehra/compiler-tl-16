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
	li $v0, 5
	syscall
	add $t0, $v0, $zero
	sw $t0, 0($fp)
	li $t0, 1
	sw $t0, -12($fp)
	lw $t1, -12($fp)
	add $t0, $t1, $zero
	sw $t0, -4($fp)
	j B2
B2:
	lw $t1, 0($fp)
	li $t2, 2
	sw $t2, -20($fp)
	lw $t3, -20($fp)
	add $t2, $t3, $zero
	slt $t0, $t1, $t2
	sw $t0, -16($fp)
	lw $t2, -16($fp)
	bne $t2, $zero, B3
L4:
	j B4
B3:
	li $t0, 0
	sw $t0, -24($fp)
	lw $t1, -24($fp)
	add $t0, $t1, $zero
	sw $t0, -4($fp)
	j B5
B4:
	lw $t1, 0($fp)
	li $t2, 1
	sw $t2, -32($fp)
	lw $t3, -32($fp)
	add $t2, $t3, $zero
	sub $t0, $t1, $t2
	sw $t0, -28($fp)
	lw $t3, -28($fp)
	add $t2, $t3, $zero
	sw $t2, -8($fp)
	j B5
B5:
	lw $t1, -8($fp)
	li $t2, 2
	sw $t2, -40($fp)
	lw $t3, -40($fp)
	add $t2, $t3, $zero
	sge $t0, $t1, $t2
	sw $t0, -36($fp)
	lw $t2, -36($fp)
	bne $t2, $zero, B6
L5:
	j B7
B6:
	j B8
B8:
	lw $t1, 0($fp)
	lw $t2, -8($fp)
	rem $t0, $t1, $t2
	sw $t0, -48($fp)
	lw $t2, -48($fp)
	add $t1, $t2, $zero
	li $t3, 0
	sw $t3, -52($fp)
	lw $t4, -52($fp)
	add $t3, $t4, $zero
	seq $t0, $t1, $t3
	sw $t0, -44($fp)
	lw $t3, -44($fp)
	bne $t3, $zero, B9
L10:
	j B10
B9:
	li $t0, 0
	sw $t0, -56($fp)
	lw $t1, -56($fp)
	add $t0, $t1, $zero
	sw $t0, -4($fp)

B10:
	lw $t1, -8($fp)
	li $t2, 1
	sw $t2, -64($fp)
	lw $t3, -64($fp)
	add $t2, $t3, $zero
	sub $t0, $t1, $t2
	sw $t0, -60($fp)
	lw $t3, -60($fp)
	add $t2, $t3, $zero
	sw $t2, -8($fp)
	j B5
B7:
B11:
	j B12
B12:
	lw $t0, -4($fp)
	bne $t0, $zero, B13
L14:
	j B14
B13:
	li $v0, 1
	li $t1, 1
	sw $t1, -68($fp)
	lw $t1, -68($fp)
	add $a0, $t1, $zero
	syscall
	li $v0, 4
	la $a0, newline
	syscall
	j B15
B14:
	li $v0, 1
	li $t1, 0
	sw $t1, -72($fp)
	lw $t1, -72($fp)
	add $a0, $t1, $zero
	syscall
	li $v0, 4
	la $a0, newline
	syscall
B15:
	j B16
B16:
	li $v0, 10
	syscall