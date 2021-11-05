% Statues public test

%  S             G   | % k=10
%  0|1|2|3|4|5|6|7   | exec(0, move), exec(1, move), exec(4, move), exec(6, move), exec(8, move), ...
% -----------------

x(0..7).

start(at(0)).
goal(at(7)).

% https://github.com/IIC2613-Inteligencia-Artificial-2021-2/Syllabus/issues/86
isRed(2).
isRed(3).
isRed(5).
isRed(7).

