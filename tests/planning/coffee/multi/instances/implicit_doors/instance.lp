% Coffee multi-agent Secret test 0

% Test moving around

%  |----| |----|
%  | o1 | | o2 |
% ---d1-+-+-d2---|
%                |
%   hallway1     |
%                |
% ---d3-+-+-d4---|
%  | o3 | | o4 |
%  |----| |----|

room(hallway1).

office(office1
      ;office2
      ;office3
      ;office4).

connected(hallway1, office1, door1).
connected(hallway1, office2, door2).
connected(hallway1, office3, door3).
connected(hallway1, office4, door4).


% Compatibility
% -------------

% There's only water
drink(water).

% Doors exist implicitly
% door(Door) :- connected(_, _, Door).

% Allow using has(Room, Drink) or delivered(Room, Drink).
holds(T, delivered(Room, Drink)) :- holds(T, has(Room, Drink)).
