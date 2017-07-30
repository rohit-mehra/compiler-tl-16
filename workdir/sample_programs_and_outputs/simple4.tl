% This program computes the Fibonacci Sequence
% It Reads the highest value to count to from the user
% It ouputs the sequence up to the user's limit

program
 var LAST as int ;
 var NEXTTOLAST as int ;
 var LIMIT as int ;
 var FIB as int ;
begin
  LIMIT := readInt ;
  LAST := 1 ;
  NEXTTOLAST := 0 ;
  FIB := 1 ;
  writeInt 0 ;   
  while FIB <= LIMIT do
   writeInt FIB ;
   FIB := LAST + NEXTTOLAST ;
   NEXTTOLAST := LAST ;
   LAST := FIB ;
  end ;
 end