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

%%% k=13
%%% MODELS=1

start(agentAt(kitchen1)).

goal(agentAt(meetingRoom1)
    ;delivered(meetingRoom1, water)
    ;delivered(meetingRoom1, coffee)
    ;delivered(meetingRoom1, tea)).

% Just enough time

% exec(0, prepare(kitchen1, water))
% exec(1, prepare(kitchen1, coffee))
% exec(2, prepare(kitchen1, tea))

% exec(3, take(kitchen1, water))
% exec(4, take(kitchen1, coffee))
% exec(5, take(kitchen1, tea))

% exec(6, open(kitchen1, doorKitchen))
% exec(7, move(kitchen1, hallway2, doorKitchen))
% exec(8, open(hallway2, doorMeetingRoom1))
% exec(9, move(hallway2, meetingRoom1, doorMeetingRoom1))

% exec(10, deliver(meetingRoom1, water))
% exec(11, deliver(meetingRoom1, coffee))
% exec(12, deliver(meetingRoom1, tea))
