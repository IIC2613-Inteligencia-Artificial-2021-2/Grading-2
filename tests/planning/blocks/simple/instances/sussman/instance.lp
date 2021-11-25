%                   |---|   |
%                   | a |   |  % k=3
%        |---|      |---|   |  exec(0, move(c,table)).
%        | c |      | b |   |  exec(1, move(b,c)).
%  |---| |---|  =>  |---|   |  exec(2, move(a,b)).
%  | b | | a |      | c |   |
% ------------------------

block( a
     ; b
     ; c).

start( on(b, table)
     ; on(a, table)
     ; on(c, a)).

goal( on(a, b)
    ; on(b, c)
    ; on(c, table)).
