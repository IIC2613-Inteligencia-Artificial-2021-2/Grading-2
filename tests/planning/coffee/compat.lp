
% Compatibility
% -------------

start(isClosed(Door)) :- door(Door),
                         not start(isOpen(Door)).

% Doors exist explicitly
door(Door) :- connected(_, _, Door).

% Allow using has(Room, Drink) or delivered(Room, Drink).
holds(T, delivered(Room, Drink)) :- holds(T, has(Room, Drink)).
