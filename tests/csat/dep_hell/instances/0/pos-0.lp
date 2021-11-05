% The original instance

requiresAtLeast(echo, libc, 1).  % `echo` uses new feature from libc v1.
requiresAtLeast(ls, libc, 0).
requiresAtMost(cat, libc, 2).    % libc v3 broke `cat`.
% installed(libc, 1).
% installed(libc, 3).

% The original request
wants( echo
     ; cat).
