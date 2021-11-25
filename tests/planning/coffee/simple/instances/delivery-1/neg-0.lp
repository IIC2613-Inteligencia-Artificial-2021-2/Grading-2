%  |----| |----|    |--------------+--------------|
%  |[R1]| | o2 |    |          mR1 |          mR2 |
% ---d1-+-+-d2---||-+-----dm1------+-----dm2------|
%                ||                               |
%                hD        h2                     |
%                ||                               |
% ---d3-+-+-d4---||--+-----dk------+-----dm3------|
%  | o3 | | o4 |     |           k |          mR3 |
%  |----| |----|     |-------------+--------------|

%%% k=8
%%% MODELS=1

start(agentAt(kitchen1)).

goal(agentAt(kitchen1)
    ;delivered(meetingRoom1, water)).

% Not enough time

% exec(0, prepare(kitchen1,water))
% exec(1, take(kitchen1,water))
% exec(2, open(kitchen1,doorKitchen))
% exec(3, move(kitchen1,hallway2))
% exec(4, open(hallway2,doorMeetingRoom1))
% exec(5, move(hallway2,meetingRoom1))
% exec(6, deliver(meetingRoom1,water))
% exec(7, move(meetingRoom1,hallway2))
% exec(8, move(hallway2,kitchen1))

