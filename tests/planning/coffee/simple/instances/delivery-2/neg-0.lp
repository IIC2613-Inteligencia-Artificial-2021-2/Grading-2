%  |----| |----|    |--------------+--------------|
%  |[R1]| | o2 |    |          mR1 |          mR2 |
% ---d1-+-+-d2---||-+-----dm1------+-----dm2------|
%                ||                               |
%                hD        h2                     |
%                ||                               |
% ---d3-+-+-d4---||--+-----dk------+-----dm3------|
%  | o3 | | o4 |     |           k |          mR3 |
%  |----| |----|     |-------------+--------------|

%%% k=9
%%% MODELS=1

start(agentAt(kitchen1)).

goal(agentAt(meetingRoom1)
    ;delivered(meetingRoom1, coffee)
    ;delivered(meetingRoom1, tea)).

% Not enough time

% exec(0, prepare(kitchen1, coffee))
% exec(1, prepare(kitchen1, tea))

% exec(2, take(kitchen1, coffee))
% exec(3, take(kitchen1, tea))

% exec(4, open(kitchen1, doorKitchen))
% exec(5, move(kitchen1, hallway2, doorKitchen))
% exec(6, open(hallway2, doorMeetingRoom1))
% exec(7, move(hallway2, meetingRoom1, doorMeetingRoom1))

% exec(8, deliver(meetingRoom1, coffee))
% exec(9, deliver(meetingRoom1, tea))

