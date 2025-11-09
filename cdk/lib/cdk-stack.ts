import * as ecs from "aws-cdk-lib/aws-ecs";
import * as ecs_patterns from "aws-cdk-lib/aws-ecs-patterns";
import * as cdk from "aws-cdk-lib/core";
import { Construct } from "constructs";
import path from "path";

export class CdkStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Constructor for load-balanced fargate service
    const fargate = new ecs_patterns.ApplicationLoadBalancedFargateService(
      this,
      "op-fargate",
      {
        cpu: 256, //0.25 of a vCPU
        memoryLimitMiB: 512,
        desiredCount: 1,
        taskImageOptions: {
          // directory of the Dockerfile
          image: ecs.ContainerImage.fromAsset(
            path.join(__dirname, "../../app")
          ),
          // port for the app in the container
          containerPort: 8080,
        },
        minHealthyPercent: 100,
        healthCheck: {
          command: [
            "CMD-SHELL",
            "curl -f http://localhost:8080/health || exit 1",
          ],
          interval: cdk.Duration.seconds(30),
          retries: 3,
          startPeriod: cdk.Duration.seconds(15),
          timeout: cdk.Duration.seconds(5),
        },
        // make it public on the internet
        publicLoadBalancer: true,
      }
    );

    // configure ALB to also use the custom healthcheck route
    fargate.targetGroup.configureHealthCheck({ path: "/health" });

    // Optional: Enable auto-scaling
    // const scaling = fargate.service.autoScaleTaskCount({
    //   minCapacity: 1,
    //   maxCapacity: 3,
    // });
    // scaling.scaleOnCpuUtilization("CpuScaling", {
    //   targetUtilizationPercent: 70,
    // });
  }
}
