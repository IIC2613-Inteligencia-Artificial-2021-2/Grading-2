{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    fish
    parallel

    python38
    python38Packages.black
    python38Packages.mypy
    python38Packages.ipython
    python38Packages.termcolor

    clingo
  ];
}
