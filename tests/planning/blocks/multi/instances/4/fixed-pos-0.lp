% Blocks-world multi-agent Secret test 4

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

%%% k=5
%%% MODELS=2

arm( a0
   ; a1).

% Closed solution

exec(0,a0,move(b0,table)).
exec(0,a1,move(b5,table)).

exec(1,a0,move(b6,b0)).
exec(1,a1,move(b1,b5)).

exec(2,a0,move(b2,b6)).
exec(2,a1,move(b7,b1)).

exec(3,a0,move(b8,b2)).
exec(3,a1,move(b3,b7)).

exec(4,a0,move(b4,b8)).
exec(4,a1,move(b9,b3)).