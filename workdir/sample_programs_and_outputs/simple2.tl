% This program takes an integer from the user as input
% It outputs 1 if the number is prime
% It outputs 0 if the number is not prime

program
 var INPUT as int ;
 var ISPRIME as bool ;
 var DIVISOR as int ;
begin
  INPUT := readInt ;
  ISPRIME := true ;
  if INPUT < 2 then
    ISPRIME := false ;
  else
    DIVISOR := INPUT - 1 ;
    while DIVISOR >= 2 do
      if INPUT mod DIVISOR = 0 then
       ISPRIME := false ;
      end ;
      DIVISOR := DIVISOR - 1 ;
    end ;
  end ;
  if ISPRIME then
   writeInt 1 ;
  else
   writeInt 0 ;
  end ;
end