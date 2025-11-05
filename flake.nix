{
  description = "AWS CDK development environment for OP Kiitorata assignment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            nodejs_18
            nodePackages.npm
            nodePackages.typescript
            awscli2
            nodePackages.aws-cdk
          ];

          shellHook = ''
            echo "AWS CDK development environment loaded"
          '';
        };
      }
    );
}
