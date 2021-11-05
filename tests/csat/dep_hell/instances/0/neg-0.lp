% Make the instance unsatisfiable
requiresAtLeast(echo, libc, 2).
requiresAtMost(echo, libc, 1).

wants(echo).
