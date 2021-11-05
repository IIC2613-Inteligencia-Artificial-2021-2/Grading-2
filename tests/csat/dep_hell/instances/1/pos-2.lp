% Dependency hell Secret test 1

% libc, 0..3
% libstdc++, 0, 1, 4
requiresAtLeast(fish, libc, 1).
requiresAtLeast(fish, libstdcpp, 0).
requiresAtMost(fish, libstdcpp, 2).
requiresAtMost(fish, libstdcpp, 2).


% Making it impossible to satisfy `ls` should not be a problem for running just `fish` right?
requiresAtLeast(ls, libstdcpp, 1).
requiresAtMost(ls, libstdcpp, 0).

wants(fish).
