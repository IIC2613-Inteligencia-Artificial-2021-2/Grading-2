% Coffee single-agent Secret test 0

%  |----| |----|    |--------------+--------------|
%  |[R1]| | o2 |    |          mR1 |          mR2 |
% ---d1-+-+-d2---||-+-----dm1------+-----dm2------|
%                ||                               |
%                hD        h2                     |
%                ||                               |
% ---d3-+-+-d4---||--+-----dk------+-----dm3------|
%  | o3 | | o4 |     |           k |          mR3 |
%  |----| |----|     |-------------+--------------|

start(agentAt(office1)).


%  |----| |----|    |--------------+--------------|
%  | o1 | | o2 |    | meetingRoom1 | meetingRoom2 |
% ---d1-+-+-d2---||-+-----dm1------+-----dm2------|
%                ||                               |
%         h1     hD        h2                     |
%                ||                               |
% ---d3-+-+-d4---||--+-----dk------+-----dm3------|
%  | o3 | | o4 |     | [R1]      k |          mR3 |
%  |----| |----|     |-------------+--------------|

goal(agentAt(hallway2)).

%%% k=4
%%% MODELS=1
