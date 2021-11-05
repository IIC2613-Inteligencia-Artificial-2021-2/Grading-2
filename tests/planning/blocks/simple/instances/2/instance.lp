% Blocks-world single-agent Secret test 2

%                                                            |
%                                                            |
%                                         |---|       |---|  |
%                                         | a |       | i |  |
%  |---| |---|       |---| |---|     =>   |---|       |---|  |
%  | a | | b | (...) | i | | j |          | b | (...) | j |  |
% ------------------------------------------------------------

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
    ; on(c, d)
    ; on(e, f)
    ; on(g, h)
    ; on(i, j)).