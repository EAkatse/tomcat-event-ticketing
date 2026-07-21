# Architecture Overview

## System Architecture

### Data Flow
1. User visits frontend (S3 + CloudFront)
2. Frontend calls API Gateway
3. API Gateway routes to Lambda
4. Lambda processes business logic
5. Lambda reads/writes to DynamoDB
6. SNS sends confirmation email
7. CloudWatch logs everything

### DynamoDB Single-Table Design

| Item Type | PK | SK | GSI1PK | GSI1SK |
|-----------|----|----|--------|--------|
| Event | EVENT#<id> | METADATA | — | — |
| Registration | EVENT#<id> | REG#<email> | REG#<email> | EVENT#<id> |

### Security Layers
- **Transport:** HTTPS (ACM + CloudFront)
- **API:** API Gateway throttling + CORS
- **Data:** DynamoDB encryption at rest
- **Access:** IAM least privilege + OIDC
- **Monitoring:** CloudWatch Alarms + SNS