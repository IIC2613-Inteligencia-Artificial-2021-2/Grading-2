% Blocks-world multi-agent Secret test 1

%                                       |
%                                       |  % k=3
%                                |---|  |  exec(0, ?, move(c,d)).
%                                | a |  |  exec(1, ?, move(b,c)).
%                                |---|  |  exec(2, ?, move(a,b)).
%                                | b |  |
%                                |---|  |
%                                | c |  |
%  |---| |---| |---| |---|  =>   |---|  |
%  | a | | b | | c | | d |       | d |  |
% ---------------------------------------

%%% k=3
%%% MODELS=2

arm( l
   ; r).

% Open solution