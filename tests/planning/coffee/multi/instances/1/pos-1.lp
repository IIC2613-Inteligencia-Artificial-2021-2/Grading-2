% Coffee multi-agent Secret test 1

%  |----| |----|    |--------------+--------------|
%  |[R1]| | o2 |    |          mR1 |          mR2 |
% ---d1-+-+-d2---||-+-----dm1------+-----dm2------|
%                ||                               |
%                hD        h2                     |
%                ||                               |
% ---d3-+-+-d4---||--+-----dk------+-----dm3------|
%  | o3 | | o4 |     |           k |          mR3 |
%  |----| |----|     |-------------+--------------|

%%% k=14
%%% MODELS=1

agent(robot1
     ;robot2).

start(agentAt(robot1, office1)
     ;agentAt(robot2, kitchen1)).

goal(delivered(office2, coffee)
    ;delivered(office3, tea)).

% 0: {robot1: {open(office1,door1)},        Agent[robot2]: {prepare(kitchen1,tea)}},
% 1: {robot1: {move(office1,hallway1)},     Agent[robot2]: {prepare(kitchen1,coffee)}},
% 2: {robot1: {open(hallway1,hallwayDoor)}, Agent[robot2]: {take(kitchen1,coffee)}},
% 3: {robot1: {move(hallway1,hallway2)},    Agent[robot2]: {open(kitchen1,doorKitchen)}},
% 4: {robot1: {move(hallway2,kitchen1)},    Agent[robot2]: {move(kitchen1,hallway2)}},
% 5: {robot1: {take(kitchen1,tea)},         Agent[robot2]: {move(hallway2,hallway1)}},
% 6: {robot1: {move(kitchen1,hallway2)},    Agent[robot2]: {open(hallway1,door2)}},
% 7: {robot1: {move(hallway2,hallway1)},    Agent[robot2]: {open(hallway1,door3)}},
% 8: {robot1: {move(hallway1,office3)},     Agent[robot2]: {move(hallway1,office2)}},
% 9: {robot1: {deliver(office3,tea)},       Agent[robot2]: {deliver(office2,coffee)}}

