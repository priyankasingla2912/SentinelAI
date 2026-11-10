# SentinelAI Deployment Guide

## 1. Overview

SentinelAI consists of:
- A Next.js frontend.
- A FastAPI backend.
- A machine-learning fraud detection model.
- A PostgreSQL database for production-oriented deployments, subject to security and readiness verification, with SQLite support for local development and testing.

This guide describes the deployment configuration identified during the project review. No specific cloud hosting provider is assumed.

## 2. Prerequisites

Before deployment, prepare:

- Python 3.11 for local backend setup.
- Node.js and npm for frontend setup.
- Docker for containerized backend deployment.
- A PostgreSQL database for production-oriented deployments, subject to security and readiness verification.
- The trained model file: `models/fraud_random_forest.pkl`.
- Required application environment variables.

Do not commit `.env` files, database credentials, JWT secrets, or other sensitive configuration to Git.

## 3. Backend Deployment

### 3.1 Local setup

From the project root:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001

```
## 3.2 Docker Deployment

The backend Dockerfile is located at `backend/Dockerfile`.

Build the Docker image from the project root:

```bash
docker build -f backend/Dockerfile -t sentinelai-backend .

```
## 4. Database Configuration

SentinelAI supports PostgreSQL for production-oriented deployments, subject to security and readiness verification, and SQLite for local development and testing.

For production:
- Configure `DATABASE_URL` with the PostgreSQL connection string.
- Keep database credentials private.
- Verify that all required database tables exist.
- Configure database backups.

Do not rely on the SQLite fallback for production deployment.

## 5. Frontend Deployment

The frontend is built with Next.js and is located in the `frontend/` directory.

Install dependencies:

```bash
npm install
```

Build the frontend:

```bash
npm run build
```

Start the production server:

```bash
npm run start
```

Configure `NEXT_PUBLIC_API_URL` with the deployed backend URL in the frontend hosting environment.

Do not use the localhost API URL as the production backend address.