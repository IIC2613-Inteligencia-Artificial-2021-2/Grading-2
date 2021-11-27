% Blocks-world single-agent Secret test 4

%  |---| |---|        |---| |---|
%  | 0 | | 5 |        | 4 | | 9 |
%  |---| |---|        |---| |---|
%  | 1 | | 6 |        | 8 | | 3 |
%  |---| |---|        |---| |---|
%  | 2 | | 7 |        | 2 | | 7 |
%  |---| |---|        |---| |---|
%  | 3 | | 8 |        | 6 | | 1 |
%  |---| |---|   =>   |---| |---|
%  | 4 | | 9 |        | 0 | | 5 |
% --------------------------------

block( b0
     ; b1
     ; b2
     ; b3
     ; b4
     ; b5
     ; b6
     ; b7
     ; b8
     ; b9).

start( on(b0, b1)
     ; on(b1, b2)
     ; on(b2, b3)
     ; on(b3, b4)
     ; on(b4, table)
     ; on(b5, b6)
     ; on(b6, b7)
     ; on(b7, b8)
     ; on(b8, b9)
     ; on(b9, table)).

goal( on(b4, b8)
    ; on(b8, b2)
    ; on(b2, b6)
    ; on(b6, b0)
    ; on(b0, table)
    ; on(b9, b3)
    ; on(b3, b7)
    ; on(b7, b1)
    ; on(b1, b5)
    ; on(b5, table)).