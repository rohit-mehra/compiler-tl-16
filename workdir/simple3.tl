% This program takes an Integer from the user
% It Returns 1 if the number is even
% It returns 0 if the number is odd
program
 var INPUT as int ;
 begin
  INPUT := readInt ;
  if INPUT > 0 then
     if INPUT mod 2 = 0 then
             writeInt  1 ;
     else
              writeInt 0 ;
     end ;     
  end ;
 end