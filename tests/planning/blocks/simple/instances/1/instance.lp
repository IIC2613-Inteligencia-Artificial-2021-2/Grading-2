% Blocks-world single-agent Secret test 1

%                                             |
%                                             |  % k=2
%                                |---||---|   |  exec(0, move(a,b)).
%                                | a || c |   |  exec(1, move(c,d)).
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