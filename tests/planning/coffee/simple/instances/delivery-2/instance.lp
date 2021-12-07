% Test preparing and delivering 2 drinks.

%  |----| |----|    |--------------+--------------|
%  | o1 | | o2 |    | meetingRoom1 | meetingRoom2 |
% ---d1-+-+-d2---||-------dm1------+-----dm2------|
%                ||                               |
%   hallway1     hD  hallway2                     |
%                ||                               |
% ---d3-+-+-d4---||--------dk------+-----dm3------|
%  | o3 | | o4 |     |   kitchen1  | meetingRoom3 |
%  |----| |----|     |-------------+--------------|

room(hallway1
    ;hallway2
    ;meetingRoom1
    ;meetingRoom2
    ;meetingRoom3).

office(office1
      ;office2
      ;office3
      ;office4).

kitchen(kitchen1).


connected(hallway1, office1, door1).
connected(hallway1, office2, door2).
connected(hallway1, office3, door3).
connected(hallway1, office4, door4).

connected(hallway1, hallway2, hallwayDoor).

connected(hallway2, meetingRoom1, doorMeetingRoom1).
connected(hallway2, meetingRoom2, doorMeetingRoom2).
connected(hallway2, meetingRoom3, doorMeetingRoom3).
connected(hallway2,     kitchen1, doorKitchen).


% There's multiple drinks
drink(water
     ;coffee
     ;tea).

