# Operations Runbook

## Deployment Process

1. Push code to `main` branch
2. GitHub Actions runs tests
3. Tests pass → SAM deploys
4. CloudFront cache invalidates (if frontend changed)
5. Smoke test runs

## Monitoring

### CloudWatch Alarms
| Alarm | Threshold | Action |
|-------|-----------|--------|
| Error Rate | > 5% | SNS email |
| Lambda Duration | > 5 seconds | SNS email |
| DynamoDB Throttling | > 0 | SNS email |

## Rollback Process

```bash
git revert HEAD
git push origin main
<<<<<<< HEAD
=======

Troubleshooting
CORS Errors
Check src/common/responses.py for CORS headers

Verify API Gateway CORS configuration

Lambda Timeouts

Increase MemorySize in template.yaml 
Optimize code (reduce external calls)
>>>>>>> 0068188 (Add SAM Event Registration API)
