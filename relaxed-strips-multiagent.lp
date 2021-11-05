% Time
% ====
time(0..k-1).


% Problem integrity checks
% ========================

% Problems must be stated correctly.
% 1. An action can't both, add and delete the same Fluent.
:- action_add(Agent, Action, Fluent),
   action_del(Agent, Action, Fluent).
% 2. A fluent cannot have a single Fluent as both, a positive and a negative precondition.
:- action_ppre(Agent, Action, Fluent),
   action_npre(Agent, Action, Fluent).


% Actions
% =======
% Agents may choose an action
0 { exec(T, Agent, Action) : action(Action) } 1 :- agent(Agent), time(T).

% Actions chosen respect the prerequisites
% Positive prerequisites
:- exec(T, Agent, Action),
   action_ppre(Agent, Action, Fluent),
   not holds(T, Fluent).
% Negative prerequisites
:- exec(T, Agent, Action),
   action_npre(Agent, Action, Fluent),
   holds(T, Fluent).

% Actions chosen by different Agents do not have clashing prerequisites
% TODO: Review if this is necessary.

% Actions chosen by different Agents do not have clashing effects
% Can collaborative actions still be modeled?
:- time(T),
   agent(Agent1),
   agent(Agent2),
   Agent1!=Agent2,
   exec(T, Agent1, Action1),
   exec(T, Agent2, Action2),
   action_add(Agent1, Action1, Fluent),
   action_add(Agent2, Action2, Fluent).
:- time(T),
   agent(Agent1),
   agent(Agent2),
   Agent1!=Agent2,
   exec(T, Agent1, Action1),
   exec(T, Agent2, Action2),
   action_del(Agent1, Action1, Fluent),
   action_del(Agent2, Action2, Fluent).


% State evolution
% ===============

% A fluent holds if it was added by the last action.
holds(T+1, Fluent) :- time(T),
                      agent(Agent),
                      exec(T, Agent, Action),
                      action_add(Agent, Action, Fluent).

% Or if it was true and it was not just made false by some action.
fluent_dropped(T, Fluent) :- time(T),
                             fluent(Fluent),
                             exec(T, Agent, Action),
                             action_del(Agent, Action, Fluent).
holds(T+1, Fluent) :- time(T),
                      agent(Agent),
                      holds(T, Fluent),
                      not fluent_dropped(T, Fluent).


% Problem definition
% ==================

% Initial state
holds(0, Fluent) :- time(0),
                    start(Fluent).
% Goal condition
:~ goal(Fluent),
   not holds(k, Fluent). [111]

% Describe only the world and the solution
#show holds/2.
#show exec/3.
