%  |----| |----|    |--------------+--------------|
%  |[R1]| | o2 |    |          mR1 |          mR2 |
% ---d1-+-+-d2---||-+-----dm1------+-----dm2------|
%                ||                               |
%                hD        h2                     |
%                ||                               |
% ---d3-+-+-d4---||--+-----dk------+-----dm3------|
%  | o3 | | o4 |     |           k |          mR3 |
%  |----| |----|     |-------------+--------------|

%%% k=6
%%% MODELS=1

start(agentAt(meetingRoom1)).

goal(agentAt(meetingRoom1)
    ;delivered(kitchen1, water)).


% It takes 7 actions, not 6.

% exec(0, open(meetingRoom1, doorMeetingRoom1))
% exec(1, move(meetingRoom1, hallway2, doorMeetingRoom1))
% exec(2, open(hallway2, doorKitchen))
% exec(3, move(hallway2, kitchen1, doorKitchen))
% exec(4, prepare(kitchen1, water))
% exec(5, move(kitchen1, hallway2, doorKitchen))
% exec(6, move(hallway2, meetingRoom1, doorKitchen))


