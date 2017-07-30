program
 var N as int;
 var TRIAL as int;
 var M as int;
 var RES as bool;
begin
   N := readInt;
   TRIAL := 2;
   RES := true;
   while TRIAL < N do
        M := N mod TRIAL;
        if M = 0 then
            RES := false;
        end;
        TRIAL := TRIAL + 1;
    end;
end