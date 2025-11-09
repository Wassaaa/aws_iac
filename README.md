# Deploy a Simple Web App with IaC

A simple web application with separate frontend and backend, deployed to AWS using Infrastructure as Code.

## Problem Interpretation and Approach

**Technology Stack:**

- **Frontend:** HTML/CSS/JavaScript (static files served by Flask)
- **Backend:** Python Flask REST API
- **Infrastructure:** AWS CDK (TypeScript)
- **Deployment:** Docker container on AWS Fargate with Application Load Balancer

**Architecture:**

- Flask serves both static frontend and API endpoints
- Frontend makes HTTP requests to backend API (demonstrates frontend <-> backend communication)
- Containerized with Docker
- Deployed to AWS Fargate (serverless containers - no EC2 management)
- Application Load Balancer provides public access
- Infrastructure fully defined as code for reproducible deployment

## Project Structure

```
/app/              - Application code
  hello.py         - Flask backend and frontend serving
  index.html       - Frontend HTML
  Dockerfile       - Container build instructions
  requirements.txt - Python dependencies
/cdk/              - Infrastructure as Code (AWS CDK)
  lib/cdk-stack.ts - Stack definition (VPC, Fargate, ALB)
  bin/cdk.ts       - CDK app entry point
```

## Build and Run Instructions

### Prerequisites

- **AWS Account** (free tier: https://aws.amazon.com/free/)
- **Node.js 24 (LTS)** and npm
- **Docker Desktop** (running)
- **AWS CLI** (https://aws.amazon.com/cli/)

**Optional - Nix users:** Run `nix develop` to get all tools automatically.

### Setup and Deploy

**1. Configure AWS credentials:**

Create an IAM user in AWS Console with `AdministratorAccess` policy (for testing - use least-privilege for production).

```bash
aws configure
```

Enter your Access Key ID, Secret Access Key, and preferred region (e.g., `eu-north-1`).

**2. Install dependencies and bootstrap CDK:**

```bash
cd cdk
npm install
npx cdk bootstrap  # One-time per AWS account/region
```

**3. Deploy:**

```bash
npx cdk deploy
```

This builds the Docker image, pushes it to ECR, and creates all AWS resources (VPC, Fargate service, Load Balancer). Takes ~5-10 minutes.

**4. Test:**

After deployment completes, look for the ALB URL in the terminal output:

```
Outputs:
CdkStack.opfargateServiceURL = http://[your-alb-url]
```

Open the URL in your browser to see the frontend, which makes requests to the backend API.

**5. Tear down (important to avoid charges):**

```bash
npx cdk destroy
```

Confirm with 'y'. This deletes all AWS resources.

## Assumptions, Trade-offs, and Known Limitations

**Assumptions:**

- Using AWS free tier resources where possible
- Single region deployment
- HTTP (not HTTPS) for simplicity

**Trade-offs:**

- **Fargate over Lambda:** Chose Fargate for simplicity (single container serves both frontend and backend). Alternative would be S3+CloudFront for frontend and Lambda+API Gateway for backend, which is cheaper but more complex infrastructure.
- **Monolithic container:** Frontend and backend in one container for simplicity. Production might separate these.
- **Administrator IAM permissions:** For ease of setup. Production should use least-privilege policies.

**Known Limitations:**

- No HTTPS/custom domain
- No CI/CD pipeline (manual deployment from local machine)
- No monitoring/alerting (CloudWatch alarms)
- Single task instance (`desiredCount: 1`) for cost efficiency - can be increased to 2+ for high availability across availability zones
- No auto-scaling configured (code included but commented out in `cdk-stack.ts`)
- No automated testing

**Idempotency:** AWS CDK ensures idempotent deployments - re-running `cdk deploy` safely updates existing resources without breaking the stack.
