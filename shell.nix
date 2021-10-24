{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    fish
    parallel
    python

    clingo
  ];
}
