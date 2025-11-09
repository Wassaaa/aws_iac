# Simple Web Application Deployed with Infrastructure as Code

A web application demonstrating frontend-backend communication and AWS deployment automation. Features a portfolio risk calculator as a practical example use case.

## Problem Interpretation and Approach

**Technology Stack:**

- **Frontend:** HTML/CSS/JavaScript single-page application
- **Backend:** Python Flask REST API with C++ calculation engine
- **Infrastructure:** AWS CDK (TypeScript)
- **Deployment:** Docker container on AWS Fargate with Application Load Balancer

**Architecture:**

- Infrastructure fully defined as code for reproducible deployment
- Multi-stage Docker build compiles C++ code and packages with Python runtime
- Deployed to AWS Fargate (serverless containers)
- Application Load Balancer provides public internet access
- Frontend provides UI for portfolio risk calculations
- JavaScript makes HTTP POST requests to Flask API (`/api/probit`)
- Flask processes requests and calls C++ binary for calculations

## Project Structure

```
/app/              - Web application
  hello.py         - Flask REST API server
  index.html       - Frontend single-page application
  Dockerfile       - Multi-stage build (C++ compilation + Python runtime)
  requirements.txt - Python dependencies
  probit/          - High-performance C++ calculation engine
    src/
      InverseCumulativeNormal.h - SIMD-optimized inverse normal CDF
      probit_api.cpp            - CLI wrapper for web API
    CMakeLists.txt - Build configuration
/cdk/              - Infrastructure as Code (AWS CDK)
  lib/cdk-stack.ts - Stack definition (VPC, Fargate, ALB)
  bin/cdk.ts       - CDK app entry point
```

## Build and Run Instructions

### Prerequisites

- **AWS Account** (free tier: https://aws.amazon.com/free/)
- **Node.js 24 (LTS)** - https://nodejs.org/en/download
- **Docker Desktop** - https://docs.docker.com/engine/install/
- **AWS CLI v2** - https://aws.amazon.com/cli/

**Optional - Nix users:** Run `nix develop` to get all tools automatically.

### Setup and Deploy

**1. Create IAM user for AWS access:**

In AWS Console:

1. Search for **IAM** → **Users** (left sidebar) → **Create user**
2. Username: `cdk-deploy` (or any name you prefer)
3. Don't enable console access → **Next**
4. **Attach policies directly** → search `AdministratorAccess` → tick it → **Next**
5. **Create user**
6. Click the new user → **Security credentials** tab → **Create access key**
7. Use case: **Command Line Interface (CLI)** → tick acknowledgment → **Next**
8. Skip description tag → **Create access key**
9. **Save both Access Key ID and Secret Access Key** (you'll need them next, you can **never** see the secret key again after you click done)

**2. Configure AWS CLI:**

```bash
aws configure
```

1. Enter your **Access** Key ID, can see in step one
2. Enter your **Secret** Access Key from step 1
3. Enter your preferred region (e.g., `eu-north-1`)
4. Enter 'json' for output format

**3. Install dependencies and bootstrap CDK:**

```bash
cd cdk
npm install
npx cdk bootstrap  # One-time per AWS account/region
```

**4. Deploy:**

```bash
npx cdk deploy
```

This builds the Docker image, pushes it to ECR, and creates all AWS resources (VPC, Fargate service, Load Balancer). Takes ~5-10 minutes.

**5. Test:**

After deployment completes, look for the ALB URL in the terminal output:

```
Outputs:
CdkStack.opfargateServiceURL = http://[your-alb-url]
```

Open the URL in your browser to see the frontend, which makes requests to the backend API.

**Example usage:**

- Enter expected return (e.g., 8.0%)
- Enter volatility (e.g., 15.0%)
- Enter confidence level (e.g., 95.0%)
- Click "Calculate Range"
- Result: "With 95% confidence, your annual return will be between -16.67% and 32.67%"

**6. Tear down (important to avoid charges):**

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

- **Fargate over Lambda:** Chose Fargate for simplicity (single container, no cold starts). Lambda+API Gateway would be cheaper for low traffic.
- **Monolithic container:** Frontend and backend in one container for simplicity. Production might separate these (S3+CloudFront for frontend).
- **Administrator IAM permissions:** For ease of setup. Production should use least-privilege policies.
- **C++ for calculations:** Demonstrates integrating compiled code with web backend. Pure Python would be simpler.

**Known Limitations:**

- No HTTPS/custom domain
- No CI/CD pipeline (manual deployment from local machine)
- No monitoring/alerting (CloudWatch alarms)
- Single task instance (`desiredCount: 1`) for cost efficiency - can be increased to 2+ for high availability
- No auto-scaling configured (code included but commented out in `cdk-stack.ts`)
- No automated testing

**Idempotency:** AWS CDK ensures idempotent deployments - re-running `cdk deploy` safely updates existing resources without breaking the stack.
