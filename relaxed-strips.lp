% Time
% ====
time(0..k-1).


% Problem integrity checks
% ========================

% Problems must be stated correctly.
% 1. An action can't both, add and delete the same Fluent.
:- action_add(Action, Fluent),
   action_del(Action, Fluent).
% 2. A fluent cannot have a single Fluent as both, a positive and a negative precondition.
:- action_ppre(Action, Fluent),
   action_npre(Action, Fluent).


% Actions
% =======
% The agent must choose an action
{ exec(T, Action) : action(Action) } = 1 :- time(T).

% Actions chosen respect the prerequisites
% Positive prerequisites
:- exec(T, Action),
   action_ppre(Action, Fluent),
   not holds(T, Fluent).
% Negative prerequisites
:- exec(T, Action),
   action_npre(Action, Fluent),
   holds(T, Fluent).


% State evolution
% ===============

% A fluent holds if it was added by the last action.
holds(T+1, Fluent) :- time(T),
                      exec(T, Action),
                      action_add(Action, Fluent).

% Or if it was true and it was not made false by the last action.
holds(T+1, Fluent) :- time(T),
                      holds(T, Fluent),
                      exec(T, Action),
                      not action_del(Action, Fluent).


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
#show exec/2.
#show simple_exec/2.

