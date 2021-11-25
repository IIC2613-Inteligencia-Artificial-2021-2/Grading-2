%  |----| |----|    |--------------+--------------|
%  | o1 | | o2 |    | meetingRoom1 | meetingRoom2 |
% ---d1-+-+-d2---||-------dm1------+-----dm2------|
%                ||                               |
%   hallway1     hD  hallway2                     |
%                ||                               |
% ---d3-+-+-d4---||--------dk------+-----dm3------|
%  | o3 | | o4 |     |   kitchen1  | meetingRoom3 |
%  |----| |----|     |-------------+--------------|

%%% k=3
%%% MODELS=1

agent(robot1
     ;robot2).

start(agentAt(robot1, office1)
     ;agentAt(robot2, office2)).

% Parallel, dependent executions (shared door opening)
goal(agentAt(robot1, office2)
    ;agentAt(robot2, office1)).
