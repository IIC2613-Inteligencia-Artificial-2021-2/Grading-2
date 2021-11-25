% Test moving around on a large map

%   |----|    |----|    |----|    |----|    |----|    |----|    |----|    |----|    |----|    |----|    |----|    |----|    |----|
%   | o0 |    | o2 |    | o4 |    | o6 |    | o8 |    |o10 |    |o12 |    |o14 |    |o16 |    |o18 |    |o20 |    |o22 |    |o24 |
% |-+-d0---||-+-d2---||-+-d4---||-+-d6---||-+-d8---||-+d10---||-+d12---||-+d14---||-+d16---||-+d18---||-+d20---||-+d22---||-+d24---|
% |        ||        ||        ||        ||        ||        ||        ||        ||        ||        ||        ||        ||        |
% |   h0  hD0   h1  hD1   h2  hD2   h3  hD3   h4  hD4   h5  hD5   h6  hD6   h7  hD7   h8  hD8   h9  hD9   h10 hD10  h11 h11   h12  |
% |        ||        ||        ||        ||        ||        ||        ||        ||        ||        ||        ||        ||        |
% |-+-d1---||-+-d3---||-+-d5---||-+-d7---||-+-d9---||-+d11---||-+d13---||-+d15---||-+d17---||-+d19---||-+d21---||-+d23---||-+d25---|
%   | o1 |    | o3 |    | o5 |    | o7 |    | o9 |    |o11 |    |o13 |    |o15 |    |o17 |    |o19 |    |o21 |    |o23 |    |o25 |
%   |----|    |----|    |----|    |----|    |----|    |----|    |----|    |----|    |----|    |----|    |----|    |----|    |----|

room(hallway0
    ;hallway1
    ;hallway2
    ;hallway3
    ;hallway4
    ;hallway5
    ;hallway6
    ;hallway7
    ;hallway8
    ;hallway9
    ;hallway10
    ;hallway11
    ;hallway12).

office(office0
      ;office1
      ;office2
      ;office3
      ;office4
      ;office5
      ;office6
      ;office7
      ;office8
      ;office9
      ;office10
      ;office11
      ;office12
      ;office13
      ;office14
      ;office15
      ;office16
      ;office17
      ;office18
      ;office19
      ;office20
      ;office21
      ;office22
      ;office23
      ;office24
      ;office25).

connected(office0, hallway0, door0).
connected(office1, hallway0, door1).
connected(hallway0, hallway1, hallwayDoor0).

connected(office2, hallway1, door2).
connected(office3, hallway1, door3).
connected(hallway1, hallway2, hallwayDoor1).

connected(office4, hallway2, door4).
connected(office5, hallway0, door5).
connected(hallway2, hallway3, hallwayDoor2).

connected(office6, hallway3, door6).
connected(office7, hallway0, door7).
connected(hallway3, hallway4, hallwayDoor3).

connected(office8, hallway4, door8).
connected(office9, hallway0, door9).
connected(hallway4, hallway5, hallwayDoor4).

connected(office10, hallway5, door10).
connected(office11, hallway5, door11).
connected(hallway5, hallway6, hallwayDoor5).

connected(office12, hallway6, door12).
connected(office13, hallway6, door13).
connected(hallway6, hallway7, hallwayDoor6).

connected(office14, hallway7, door14).
connected(office15, hallway7, door15).
connected(hallway7, hallway8, hallwayDoor7).

connected(office16, hallway8, door16).
connected(office17, hallway8, door17).
connected(hallway8, hallway9, hallwayDoor8).

connected(office18, hallway9, door18).
connected(office19, hallway9, door19).
connected(hallway9, hallway10, hallwayDoor9).

connected(office20, hallway10, door20).
connected(office21, hallway10, door21).
connected(hallway10, hallway11, hallwayDoor10).

connected(office22, hallway11, door22).
connected(office23, hallway11, door23).
connected(hallway11, hallway12, hallwayDoor11).

connected(office24, hallway12, door24).
connected(office25, hallway12, door25).




% Compatibility
% -------------

% There's only water
drink(water).
% Doors exist explicitly
door(Door) :- connected(_, _, Door).

% Allow using has(Room, Drink) or delivered(Room, Drink).
holds(T, delivered(Room, Drink)) :- holds(T, has(Room, Drink)).