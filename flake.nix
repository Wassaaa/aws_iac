{
  description = "AWS CDK development environment for OP Kiitorata assignment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      nixpkgs,
      flake-utils,
      ...
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            nodejs_24
            awscli2
            python313
            python313Packages.flask
            python313Packages.pip
          ];

          shellHook = ''
            echo "AWS CDK development environment loaded"
          '';
        };
      }
    );
}
