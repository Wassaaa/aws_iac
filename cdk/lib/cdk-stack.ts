import * as apigateway from "aws-cdk-lib/aws-apigateway";
import * as lambda from "aws-cdk-lib/aws-lambda-nodejs";
import * as cdk from "aws-cdk-lib/core";
import { Construct } from "constructs";
import * as path from "path";

export class CdkStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const helloFunction = new lambda.NodejsFunction(this, "HelloFunction", {
      entry: path.join(__dirname, "../../lambda/hello/index.ts"),
    });

    new apigateway.LambdaRestApi(this, "HelloApi", {
      handler: helloFunction,
      description: "Simple REST API for OP Kiitorata assignment",
    });
  }
}
