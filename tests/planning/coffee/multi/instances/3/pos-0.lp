% Coffee multi-agent Secret test 3

%  |----| |----|    |--------------+--------------|
%  |[R1]| | o2 |    |          mR1 |          mR2 |
% ---d1-+-+-d2---||-+-----dm1------+-----dm2------|
%                ||                               |
%                hD        h2                     |
%                ||                               |
% ---d3-+-+-d4---||--+-----dk------+-----dm3------|
%  | o3 | | o4 |     |           k |          mR3 |
%  |----| |----|     |-------------+--------------|

%%% k=15
%%% MODELS=1

agent(robot1).

start(agentAt(robot1, kitchen1)).

goal(delivered(meetingRoom1, water)
    ;delivered(meetingRoom2, water)).

% Just enough time

% robot1: exec(0, prepare(kitchen1, water))
% robot1: exec(1, take(kitchen1, water))
% robot1: exec(2, open(kitchen1, doorKitchen))
% robot1: exec(3, move(kitchen1, hallway2, doorKitchen))
% robot1: exec(4, open(hallway2, doorMeetingRoom1))
% robot1: exec(5, move(hallway2, meetingRoom1, doorMeetingRoom1))
% robot1: exec(6, deliver(meetingRoom1, water))

% robot1: exec(7, move(meetingRoom1, hallway2, doorMeetingRoom1))
% robot1: exec(8, move(hallway2, kitchen1, doorKitchen))

% robot1: exec(9, prepare(kitchen1, water))
% robot1: exec(10, take(kitchen1, water))
% robot1: exec(11, move(kitchen1, hallway2, doorKitchen))
% robot1: exec(12, open(hallway2, doorMeetingRoom2))
% robot1: exec(13, move(hallway2, meetingRoom2, doorMeetingRoom2))
% robot1: exec(14, deliver(meetingRoom2, water))
