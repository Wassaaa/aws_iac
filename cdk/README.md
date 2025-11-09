# CDK Infrastructure

This directory contains the AWS CDK (TypeScript) infrastructure code for deploying the portfolio risk calculator to AWS.

## What This Deploys

- **VPC**: Default VPC with public/private subnets
- **ECS Fargate Service**: Runs the Docker container (0.25 vCPU, 512 MB memory)
- **Application Load Balancer**: Public-facing HTTP endpoint
- **ECR**: Container registry for Docker images
- **Security Groups**: Configured for HTTP traffic

The stack is defined in `lib/cdk-stack.ts` and uses a single Fargate task (`desiredCount: 1`) for cost efficiency.

## Commands

- `npm install` install dependencies
- `npx cdk bootstrap` one-time setup per AWS account/region
- `npx cdk deploy` deploy this stack to your default AWS account/region
- `npx cdk destroy` tear down all resources
- `npx cdk diff` compare deployed stack with current state
- `npx cdk synth` emits the synthesized CloudFormation template
