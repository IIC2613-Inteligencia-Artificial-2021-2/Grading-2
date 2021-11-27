%                                                |
%                                         |---|  |
%                                         | a |  |
%                                         |---|  |
%                                         | b |  |
%                                         |---|  |
%                                         |...|  |
%                                         |---|  |
%                                         | i |  |
%  |---| |---|       |---| |---|     =>   |---|  |
%  | a | | b | (...) | i | | j |          | j |  |
% ------------------------------------------------

block( a
     ; b
     ; c
     ; d
     ; e
     ; f
     ; g
     ; h
     ; i
     ; j).

start( on(a, table)
     ; on(b, table)
     ; on(c, table)
     ; on(d, table)
     ; on(e, table)
     ; on(f, table)
     ; on(g, table)
     ; on(h, table)
     ; on(i, table)
     ; on(j, table)).

goal( on(a, b)
    ; on(b, c)
    ; on(c, d)
    ; on(d, e)
    ; on(e, f)
    ; on(f, g)
    ; on(g, h)
    ; on(h, i)
    ; on(i, j)).
