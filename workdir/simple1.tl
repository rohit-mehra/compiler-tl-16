% sqrt.tl
% This is a program that approximates a sqrt to the smallest
% integer less than the square root by trying each possible sqrt
% until it finds one that is too large

program
  var N as int ;
  var SQRT as int ;
begin
  N := readInt ;
  SQRT := 0 ;

  % go until SQRT exceeds the square root of N
  while SQRT * SQRT <= N do
    SQRT := SQRT + 1 ;
  end ;

  SQRT := SQRT - 1 ; % subtract one SQRT is <= sqrt(N)

  writeInt SQRT ;

end
