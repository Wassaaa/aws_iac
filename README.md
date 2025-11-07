# Assignment 3: Deploy a Simple Web App with IaC

This project uses AWS CDK (TypeScript) to deploy a simple Python Flask web application to AWS.

The app runs in a Docker container on AWS Fargate with an Application Load Balancer (ALB) that makes it accessible from the internet.

## Problem Interpretation and Approach

**Technology choice:** AWS CDK with TypeScript (matches the preferred stack from the assignment)

**Why Fargate instead of Lambda?**

For a simple, low-traffic app, AWS Lambda would be cheaper and easier. However, I chose Fargate because:

- Quantitative applications (like pricing model APIs) often need to run continuously
- Fargate handles long-running services better than Lambda
- Shows understanding of containerized deployment patterns
- More realistic for production workloads

**Architecture:**

- Python Flask app in a Docker container
- AWS Fargate (serverless containers - no EC2 servers to manage)
- Application Load Balancer for public access
- Two-layer health check system for high availability

## Project Structure

```
/app/           - Python Flask application
  hello.py      - Main application code
  Dockerfile    - Container build instructions
  requirements.txt - Python dependencies
/cdk/           - AWS CDK infrastructure code (TypeScript)
  lib/cdk-stack.ts - Stack definition
  bin/cdk.ts    - CDK app entry point
```

## Build and Run Instructions

### Prerequisites

- Node.js 24 (LTS) and npm
- Docker Desktop (running)
- AWS CLI installed

**Alternative (Nix users):** If you have the Nix package manager installed, you can use the included `flake.nix`:

```bash
nix develop
```

This automatically provides Node.js 24 and AWS CLI in a reproducible environment.

### Step 1: AWS Account Setup (One-time)

1. **Create AWS Account:** Sign up at aws.amazon.com

2. **Create IAM User:**

   - Open AWS Console → IAM service
   - Create new User
   - Attach policy: `AdministratorAccess` (Note: This gives full access - only for testing. For production, use limited permissions.)
   - Save the `Access Key ID` and `Secret Access Key`

3. **Configure AWS CLI:**
   ```bash
   aws configure
   ```
   Enter your Access Key ID and Secret Access Key when asked.
   Choose a region (e.g., `eu-north-1` for Stockholm)

### Step 2: Deploy

1. **Navigate to CDK directory:**

   ```bash
   cd cdk
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```

3. **Bootstrap CDK (one-time per AWS account/region):**

   ```bash
   npx cdk bootstrap
   ```

   This creates the S3 buckets and IAM roles that CDK needs.

4. **Deploy the stack:**

   ```bash
   npx cdk deploy
   ```

   This will:

   - Build the Docker image locally
   - Push it to AWS ECR (container registry)
   - Create VPC, Load Balancer, Fargate service
   - Takes about 5-10 minutes

5. **Test the application:**
   - Look for `Outputs:` in the terminal after deployment finishes
   - Copy the URL
   - Open it in your browser or use curl:
     ```bash
     curl http://[your-url]
     ```
   - You should see JSON: `{"message":"Hello from my Fargate container!","timestamp":"..."}`
   - Health check endpoint: `http://[your-url]/health`

### Step 3: Clean Up

**Important:** To delete all AWS resources and stop charges:

```bash
npx cdk destroy
```

Confirm with 'y' when asked.

## Assumptions, Trade-offs, and Design Decisions

### Two-Layer Health Check System

This deployment uses two health checks on the `/health` endpoint:

1. **ALB Health Check** (configured via `targetGroup.configureHealthCheck`)

   - Purpose: Traffic routing decision
   - If unhealthy: ALB stops sending traffic to the container
   - Interval: 30 seconds

2. **ECS Health Check** (configured via `healthCheck` in task definition)
   - Purpose: Container restart decision
   - If unhealthy: ECS kills and replaces the container (self-healing)
   - Uses `curl` command inside the container

**Why curl in Dockerfile?** The ECS health check runs `curl` inside the container, so I installed it with `apt-get install curl`. This is a standard approach for container health checks.

### Trade-offs

**Chosen: Fargate**

- ✅ Always-on, no cold starts
- ✅ More realistic for production APIs
- ❌ Higher cost (~\$5-10/month vs Lambda's near-$0 for low traffic)

**Alternative: Lambda + API Gateway**

- ✅ Much cheaper for low traffic
- ✅ Auto-scales to zero
- ❌ Cold start delays (100-500ms)
- ❌ Less suitable for always-on services

### Known Limitations

- **No CI/CD pipeline:** Deployment is manual from local machine. For production, should use `aws-cdk-lib/pipelines` for automated deployments.
- **No monitoring/alerting:** No CloudWatch alarms for errors or high latency.
- **Single container:** No redundancy (minHealthyPercent: 100 means only one task). For production, should run multiple tasks.
- **No custom domain:** Uses default ALB URL.
- **Administrator access:** IAM setup uses full admin permissions for simplicity. Production should use least-privilege policies.

### Testing

- Manual testing via browser and curl
- Health check endpoints verified via CloudWatch logs
