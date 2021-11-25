%  |----| |----|    |--------------+--------------|
%  | o1 | | o2 |    |          mR1 |          mR2 |
% ---d1-+-+-d2---||-+-----dm1------+-----dm2------|
%                ||                               |
%                hD        h2                     |
%                ||                               |
% ---d3-+-+-d4---||--+-----dk------+-----dm3------|
%  | o3 | | o4 |     |  [R1]     k |          mR3 |
%  |----| |----|     |-------------+--------------|

%%% k=15
%%% MODELS=1

start(agentAt(kitchen1)).

goal(delivered(meetingRoom1, water)
    ;delivered(meetingRoom2, water)).

% Just enough time

% exec(0, prepare(kitchen1, water))
% exec(1, take(kitchen1, water))
% exec(2, open(kitchen1, doorKitchen))
% exec(3, move(kitchen1, hallway2, doorKitchen))
% exec(4, open(hallway2, doorMeetingRoom1))
% exec(5, move(hallway2, meetingRoom1, doorMeetingRoom1))
% exec(6, deliver(meetingRoom1, water))

% exec(7, move(meetingRoom1, hallway2, doorMeetingRoom1))
% exec(8, move(hallway2, kitchen1, doorKitchen))

% exec(9, prepare(kitchen1, water))
% exec(10, take(kitchen1, water))
% exec(11, move(kitchen1, hallway2, doorKitchen))
% exec(12, open(hallway2, doorMeetingRoom2))
% exec(13, move(hallway2, meetingRoom2, doorMeetingRoom2))
% exec(14, deliver(meetingRoom2, water))
