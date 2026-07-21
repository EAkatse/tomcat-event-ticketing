# Event Registration & Ticketing System

A serverless REST API for event registration and ticketing, built with AWS Lambda, API Gateway, and DynamoDB.

## Architecture Overview
Browser │────▶│ CloudFront │────▶│ API Gateway│────▶│ Lambda
│
▼
┌─────────────┐
│ DynamoDB │
│ (Single- │
│ Table) │
└─────────────┘


## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /register | Register for an event |
| GET | /events | List all events |
| GET | /registrations/{email} | View registrations by email |
| DELETE | /registration/{id} | Cancel a registration |

## Tech Stack

- **Compute:** AWS Lambda (Python 3.12)
- **API:** Amazon API Gateway (REST)
- **Database:** Amazon DynamoDB (Single-table design)
- **CI/CD:** GitHub Actions with OIDC
- **Monitoring:** Amazon CloudWatch + SNS
- **Cost Control:** AWS Budgets

## Project Structure

event-ticketing-api/
├── .github/workflows/ # CI/CD pipelines
├── src/handlers/ # Lambda function code
├── infra/ # SAM nested stacks
├── tests/ # Unit + integration tests
├── docs/ # Documentation
├── template.yaml # SAM root stack
└── README.md # This file



## Getting Started

### Prerequisites
- AWS CLI configured
- SAM CLI installed
- Python 3.12+
- Git

### Local Development

```bash
# Clone the repository
git clone https://github.com/EAkatse/tomcat-event-ticketing.git
cd tomcat-event-ticketing

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt

# Start local API
sam local start-api

Live Deployment
Frontend: https://xxxxxxxxxxxxxxx.com
API: https://api.xxxxxxxxxxxxxxxxxxx.com
GitHub: https://github.com/EAkatse/tomcat-event-ticketing.git 


Team
Role	Name
Team Coordinator	[David Quayartey]
CI/CD Manager	[Samuel Kinsford Amoah]
Backend Engineer	[Peter Nartey]
Database Admin	[Emmanuel Akatse]
Monitoring Lead [Nunoo Annah Frimpomaah]
Quality Assurance Lead [Salu Alhassan]