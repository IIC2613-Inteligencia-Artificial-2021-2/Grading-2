
wants(ncmpcpp).

% libc: 0..2
requiresAtLeast(ncmpcpp, libc, 2).

% libmpdclient 0..2
requiresAtMost(ncmpcpp, libmpdclient, 1).

% libpthread 0
requiresAtLeast(ncmpcpp, libpthread, 0).

% libncursesw 0..6
requiresAtLeast(ncmpcpp, libncursesw, 4).

% libcurl 0..4
requiresAtLeast(ncmpcpp, libcurl, 4).

% libresolv 0..2
requiresAtLeast(ncmpcpp, libresolv, 2).

% libreadline 0..5
requiresAtLeast(ncmpcpp, libreadline, 1).

% libstdcpp 0..6
requiresAtLeast(ncmpcpp, libstdcpp, 2).

% libgcc 0
requiresAtMost(ncmpcpp, libgcc, 0).

% libssh 0..1
requiresAtLeast(ncmpcpp, libssh, 0).

% libssl 0..1
requiresAtLeast(ncmpcpp, libssl, 0).

% libcrypto 0..1
requiresAtLeast(ncmpcpp, libcrypto, 1).
