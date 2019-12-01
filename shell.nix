{ pkgs ? import <nixpkgs> {} }:

with pkgs;

let
	pyEnv = python37.withPackages (ps: with ps; [
		pylint numpy
	]);
in mkShell {
	name = "aoc2019";
	buildInputs = [ 
		pyEnv
	];
}
