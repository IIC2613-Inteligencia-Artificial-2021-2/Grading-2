%                                            |
%                                     |---|  |
%                                     | a |  |
%                                     |---|  |
%                                     | b |  |
%                                     |---|  |
%                                     | c |  |
%                                     |---|  |
%                                     | d |  |
%  |---||---||---||---||---|     =>   |---|  |
%  | a || b || c || d || e |          | e |  |
% ---------------------------------------------

block( a
     ; b
     ; c
     ; d
     ; e).

start( on(a, table)
     ; on(b, table)
     ; on(c, table)
     ; on(d, table)
     ; on(e, table)).

goal( on(a, b)
    ; on(b, c)
    ; on(c, d)
    ; on(d, e)).
