%                                       |
%                                       |  % k=3
%                                |---|  |  exec(0, ?, move(c,d)).
%                                | a |  |  exec(1, ?, move(b,c)).
%                                |---|  |  exec(2, ?, move(a,b)).
%                                | b |  |
%                                |---|  |
%                                | c |  |
%  |---| |---| |---| |---|  =>   |---|  |
%  | a | | b | | c | | d |       | d |  |
% ---------------------------------------

block( a
     ; b
     ; c
     ; d).

start( on(a, table)
     ; on(b, table)
     ; on(c, table)
     ; on(d, table)).

goal( on(a, b)
    ; on(b, c)
    ; on(c, d)
    ; on(d, table)).