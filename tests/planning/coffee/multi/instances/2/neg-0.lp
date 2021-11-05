% Coffee multi-agent Secret test 2

%  |----| |----|    |--------------+--------------|
%  |[R1]| | o2 |    |          mR1 |          mR2 |
% ---d1-+-+-d2---||-+-----dm1------+-----dm2------|
%                ||                               |
%                hD        h2                     |
%                ||                               |
% ---d3-+-+-d4---||--+-----dk------+-----dm3------|
%  | o3 | | o4 |     |           k |          mR3 |
%  |----| |----|     |-------------+--------------|

%%% k=12
%%% MODELS=1

agent(robot1
     ;robot2).

start(agentAt(robot1, office1)
     ;agentAt(robot2, kitchen1)).

goal(delivered(office1, water)
    ;delivered(office2, coffee)
    ;delivered(office3, tea)).

%  0: {robot1: open(office1,door1),        robot2: prepare(kitchen1,water)}
%  1: {robot1: move(office1,hallway1),     robot2: prepare(kitchen1,coffee)}
%  2: {robot1: open(hallway1,hallwayDoor), robot2: prepare(kitchen1,tea)}
%  3: {robot1: move(hallway1,hallway2),    robot2: take(kitchen1,water)}
%  4: {robot1: open(hallway2,doorKitchen), robot2: take(kitchen1,tea)}
%  5: {robot1: move(hallway2,kitchen1),    robot2: move(kitchen1,hallway2)}
%  6: {robot1: take(kitchen1,coffee),      robot2: move(hallway2,hallway1)}
%  7: {robot1: move(kitchen1,hallway2),    robot2: move(hallway1,office1)}
%  8: {robot1: move(hallway2,hallway1),    robot2: deliver(office1,water)}
%  9: {robot1: open(hallway1,door3),       robot2: move(office1,hallway1)}
% 10: {robot1: open(hallway1,door2),       robot2: move(hallway1,office3)}
% 11: {robot1: move(hallway1,office2),     robot2: deliver(office3,tea)}
% 12: {robot1: deliver(office2,coffee),    robot2: -                   }
