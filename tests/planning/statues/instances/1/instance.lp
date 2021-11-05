% Statues Secret test 1

%  S G   | % k=10
%  0|1|  | exec(0, wait), exec(1, move), exec(4, move), exec(6, move), exec(8, move), ...
% --------
x(0..1).

start(at(0)).
goal(at(1)).

isRed(0).
isRed(1).
