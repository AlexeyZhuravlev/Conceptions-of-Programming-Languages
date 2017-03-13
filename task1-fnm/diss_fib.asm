funcb 1
mov 3 *1
add 3 1
mov 4 **3
mov 5 *4
sub 5 1
rjgz *5 5
mov 2 *4
mov 3 **1
pop
jump *3
push *5
call 1
mov 5 **1
pop
sub 5 1
push *2
push *5
call 1
pop
add 2 **1
pop
mov 3 **1
pop
jump *3
funce
read 3
push *3
call 1
pop
print *2
term
