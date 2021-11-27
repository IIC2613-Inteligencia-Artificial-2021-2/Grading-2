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

%%% k=5
%%% MODELS=2

arm( a0
   ; a1).

% Open solution without enough time, but enough time iligal plans,
% 0: {Agent[a0]: {move(i,j)}, Agent[a1]: {move(h,i)}}
% 1: {Agent[a0]: {move(g,h)}, Agent[a1]: {move(f,g)}}
% 3: {Agent[a0]: {move(d,e)}, Agent[a1]: {move(e,f)}}
% 4: {Agent[a0]: {move(c,d)}, Agent[a1]: {move(c,d)}}
% 5: {Agent[a0]: {move(a,b)}, Agent[a1]: {move(b,c)}}
