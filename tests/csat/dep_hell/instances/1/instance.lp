% Dependency hell Secret test 1

program( echo
       ; cat
       ; fish
       ; ls).
version(libc, 0).
version(libc, 1).
version(libc, 2).
version(libc, 3).

version(libstdcpp, 0).
version(libstdcpp, 1).
% No one relies on these being adjacent numbers, right?
% version(libstdcpp, 2).
% version(libstdcpp, 3).
version(libstdcpp, 4).

version(libpthread, 0).
version(libpthread, 1).
