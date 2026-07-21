# Event Registration & Ticketing System

A serverless event registration and ticketing API built with AWS Lambda, API Gateway, and DynamoDB. This system replaces manual Microsoft Forms + Excel workflows with an automated, scalable solution.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Local Development](#local-development)
- [Deployment](#deployment)
- [Monitoring & Alarms](#monitoring--alarms)
- [Team](#team)
- [Links](#links)

---

## Project Overview

**Problem:** An event management organization is struggling to handle growing registration volumes using a manual system built on Microsoft Forms and Excel spreadsheets. The operations team lacks automated workflows for attendee confirmation emails, real-time system monitoring, and a structured deployment process.

**Solution:** A serverless REST API that automates event ticketing, provides strict cost tracking within the Free Tier, and streamlines developer updates through a CI/CD pipeline.

**Key Features:**
- Register for events
- List all available events
- View registrations by email
- Cancel registrations
- Automated confirmation emails
- Real-time monitoring and alerts

---

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              End Users (Browser)                            │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CloudFront (CDN) + S3 (Static Frontend)                  │
│                         https://eventregistration.com                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Amazon API Gateway (REST API)                        │
│                   POST /register | GET /events | GET /registrations         │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           AWS Lambda (Python 3.12)                          │
│                     Business logic for each endpoint                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      Amazon DynamoDB (Single-Table Design)                  │
│                         Events & Registrations                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│              Amazon SNS (Confirmation Emails) + CloudWatch (Monitoring)      │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Data Flow

1. User visits frontend website (hosted on S3 + CloudFront)
2. Frontend makes API calls to API Gateway
3. API Gateway routes requests to appropriate Lambda function
4. Lambda processes business logic:
   - Validates input
   - Reads/writes to DynamoDB
   - Triggers SNS for confirmation emails
5. CloudWatch logs everything and triggers alarms if errors exceed threshold

### DynamoDB Single-Table Design

| Item Type | PK | SK | GSI1PK | GSI1SK |
|-----------|----|----|--------|--------|
| Event | `EVENT#<eventId>` | `METADATA` | — | — |
| Registration | `EVENT#<eventId>` | `REG#<email>` | `REG#<email>` | `EVENT#<eventId>` |

**Access Patterns:**
- Get all registrations for an event: `Query(PK = "EVENT#<id>")`
- Get all registrations for an email: `Query(GSI1PK = "REG#<email>")`

---

## Tech Stack

| Service | Purpose |
|---------|---------|
| **AWS Lambda** | Serverless compute for business logic (Python 3.12) |
| **Amazon API Gateway** | REST API endpoints with CORS and throttling |
| **Amazon DynamoDB** | NoSQL database with single-table design |
| **Amazon CloudFront** | CDN for frontend static assets |
| **Amazon S3** | Static frontend hosting |
| **Amazon SNS** | Confirmation email notifications |
| **Amazon CloudWatch** | Logging, monitoring, and alarms |
| **AWS IAM** | Least-privilege access control |
| **AWS Budgets** | Cost tracking and alerts |
| **GitHub Actions** | CI/CD pipeline with OIDC authentication |
| **AWS SAM** | Infrastructure as Code (nested stacks) |

---

## API Endpoints

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| **POST** | `/register` | Register for an event | `{ "event_id": "evt123", "email": "user@email.com", "name": "John" }` | `{ "registration_id": "reg456", "status": "confirmed" }` |
| **GET** | `/events` | List all available events | — | `{ "events": [ { "id": "evt123", "name": "AWS Workshop", "date": "2026-08-15", "capacity": 100 } ] }` |
| **GET** | `/registrations/{email}` | View registrations by email | — | `{ "registrations": [ { "event_id": "evt123", "event_name": "AWS Workshop", "status": "confirmed" } ] }` |
| **DELETE** | `/registration/{id}` | Cancel a registration | — | `{ "message": "Registration cancelled successfully" }` |

---

## Project Structure

```
event-ticketing-api/
├── .github/
│   ├── workflows/
│   │   ├── pr-validation.yml       # Lint + unit tests on PR
│   │   ├── deploy.yml              # Build + deploy on push to main
│   │   └── destroy-stack.yml       # Manual stack teardown
│   ├── CODEOWNERS                  # Path-to-owner mappings
│   └── PULL_REQUEST_TEMPLATE.md    # PR template
├── src/
│   ├── handlers/
│   │   ├── register/               # POST /register Lambda
│   │   │   ├── app.py
│   │   │   └── requirements.txt
│   │   ├── list_events/            # GET /events Lambda
│   │   │   ├── app.py
│   │   │   └── requirements.txt
│   │   ├── get_registrations/      # GET /registrations/{email} Lambda
│   │   │   ├── app.py
│   │   │   └── requirements.txt
│   │   └── cancel_registration/    # DELETE /registration/{id} Lambda
│   │       ├── app.py
│   │       └── requirements.txt
│   └── common/
│       ├── db.py                   # Shared DynamoDB client
│       ├── responses.py            # Standardized responses + CORS
│       └── validation.py           # Input validation
├── infra/
│   ├── dynamodb.yaml               # DynamoDB table + GSI
│   ├── api-gateway.yaml            # API Gateway + CORS + throttling
│   ├── monitoring.yaml             # CloudWatch alarms + dashboard
│   └── budgets.yaml                # AWS Budgets + alerts
├── tests/
│   ├── unit/                       # Unit tests for each handler
│   └── integration/                # API smoke tests
├── docs/
│   ├── ARCHITECTURE.md             # Detailed architecture docs
│   ├── RUNBOOK.md                  # Operations runbook
│   └── openapi.yaml                # OpenAPI specification
├── scripts/
│   ├── seed_events.py              # Seed data for local dev
│   └── local_invoke.sh             # SAM local invoke wrapper
├── template.yaml                   # SAM root stack
├── samconfig.toml                  # SAM deployment config
├── requirements-dev.txt            # Dev dependencies
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites

- AWS CLI configured with appropriate permissions
- AWS SAM CLI installed
- Python 3.12+
- Git
- GitHub account with repository access

### Clone the Repository

```bash
git clone https://github.com/EAkatse/tomcat-event-ticketing.git
cd tomcat-event-ticketing
```

### Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
```

---

## Local Development

### Run API Locally with SAM

```bash
sam local start-api
```

This starts a local API Gateway on `http://localhost:3000`.

### Test Endpoints

```bash
# List events
curl http://localhost:3000/events

# Register for an event
curl -X POST http://localhost:3000/register \
  -H "Content-Type: application/json" \
  -d '{"event_id":"evt123","email":"user@email.com","name":"John"}'
```

### Run Unit Tests

```bash
pytest tests/unit --cov=src --cov-report=term-missing
```

### Run Integration Tests

```bash
pytest tests/integration/
```

---

## Deployment

### Deploy via GitHub Actions (Automated)

1. Push code to `main` branch
2. GitHub Actions automatically:
   - Runs linting and unit tests
   - Builds SAM application
   - Deploys to AWS
   - Runs smoke tests

### Deploy Manually with SAM

```bash
sam build --use-container
sam deploy --stack-name event-ticketing-api-prod \
  --capabilities CAPABILITY_IAM \
  --resolve-s3 \
  --parameter-overrides Environment=prod
```

### Destroy Stack (Manual)

```bash
aws cloudformation delete-stack --stack-name event-ticketing-api-prod
```

---

## Monitoring & Alarms

### CloudWatch Logs

| Log Group | Purpose |
|-----------|---------|
| `/aws/lambda/register` | Registration endpoint logs |
| `/aws/lambda/list_events` | Events listing logs |
| `/aws/lambda/get_registrations` | Registration viewing logs |
| `/aws/lambda/cancel_registration` | Cancellation logs |

### CloudWatch Alarms

| Alarm | Threshold | Action |
|-------|-----------|--------|
| **High Error Rate** | Error rate > 5% | SNS email notification |
| **Lambda Duration** | Duration > 5 seconds | SNS email notification |
| **DynamoDB Throttling** | Throttled requests > 0 | SNS email notification |

### AWS Budgets

| Budget | Threshold | Alert |
|--------|-----------|-------|
| **Monthly Cost** | $5.00 | 80% and 100% email alerts |

---

## Team

| Role | Name | GitHub Username | Responsibilities |
|------|------|-----------------|------------------|
| **Team Coordinator** | David Quayartey | @dquayartey | Architecture, coordination, documentation, domain/DNS |
| **CI/CD Manager** | Samuel Kingsford Amoah | @KingsCreatives | GitHub Actions, OIDC, deployment automation |
| **Backend Engineer** | Peter Nartey | @plnartey | POST /register, DELETE /registration Lambdas |
| **Database Admin** | Emmanuel Akatse | @EAkatse | GET /events, GET /registrations, DynamoDB design |
| **Monitoring Lead** | Nunoo Annah Frimpomaah | @Cyber-nunoo | CloudWatch, IAM, SNS, Budgets |
| **Quality Assurance Lead** | Salu Alhassan | @SAlhassan | Testing, OpenAPI, README, demo |

---

## Links

| Resource | URL |
|----------|-----|
| **GitHub Repository** | https://github.com/EAkatse/tomcat-event-ticketing |
| **Trello Board** | https://trello.com/b/GWJVHvuQ/tomcat-project-2 |
| **Live Frontend** | https://www.xxxxxxxx.com |
| **API Base URL** | https://[api-id].execute-api.[region].amazonaws.com/prod |
| **Architecture Diagram** | [Link to diagram] |
| **OpenAPI Specification** | `docs/openapi.yaml` |

---

## License

This project is part of the Azubi Africa AWS Cloud Program.

---
