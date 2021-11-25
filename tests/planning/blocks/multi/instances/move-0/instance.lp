%                                             |
%                                             |  % k=1
%                                |---||---|   |  exec(0, l, move(a,b)).
%                                | a || c |   |  exec(0, r, move(c,d)).
%  |---| |---| |---| |---|  =>   |---||---|   |
%  | a | | b | | c | | d |       | b || d |   |
% ------------------------------------------

block( a
     ; b
     ; c
     ; d).

start( on(a, table)
     ; on(b, table)
     ; on(c, table)
     ; on(d, table)).

goal( on(a, b)
    ; on(c, d)).
