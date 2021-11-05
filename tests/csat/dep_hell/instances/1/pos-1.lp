% Dependency hell Secret test 1

% libc, 0..3
% libstdc++, 0, 1, 4
requiresAtLeast(fish, libc, 1).
requiresAtLeast(fish, libstdcpp, 0).
requiresAtMost(fish, libstdcpp, 2).
requiresAtMost(fish, libstdcpp, 2).


wants(fish).
