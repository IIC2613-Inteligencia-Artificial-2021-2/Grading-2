%                                             |
%                                             |  % k=1
%                                |---||---|   |  exec(0, l, move(a,b)).
%                                | a || c |   |  exec(0, r, move(c,d)).
%  |---| |---| |---| |---|  =>   |---||---|   |
%  | a | | b | | c | | d |       | b || d |   |
% ------------------------------------------


%%% k=1
%%% MODELS=2

arm( armA
   ; armB
   ; armC
   ; armD
   ; armE).

% Open solution with extra arms
