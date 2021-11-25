%                                             |
%                                             |  % k=1
%                                |---||---|   |  exec(0, l, move(a,b)).
%                                | a || c |   |  exec(0, r, move(c,d)).
%  |---| |---| |---| |---|  =>   |---||---|   |
%  | a | | b | | c | | d |       | b || d |   |
% ------------------------------------------


%%% k=1
%%% MODELS=2

arm( l
   ; r).

% Partial screwup, now there's not enough time

exec(0, l, move(b, a)).
