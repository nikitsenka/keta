# KETA Setup Guide

## Prerequisites

- Python 3.12+
- Node.js 20+
- Docker and Docker Compose
- OpenAI API Key

## Quick Start

### 1. Clone and Setup Environment

```bash
# Create .env file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your_key_here
```

### 2. Start with Docker Compose

```bash
# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

This will start:
- PostgreSQL with Apache AGE on port 5432
- FastAPI backend on port 8000
- React frontend on port 5173

### 3. Verify Installation

```bash
# Check API health
curl http://localhost:8000/health

# Check database
docker exec keta-postgres psql -U postgres -d keta_db -c "\dt keta.*"
```

### 4. Access the Application

- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs
- **API**: http://localhost:8000/api/v1

## Manual Setup (Development)

### Backend Setup

```bash
# Install Python dependencies
pip install -e ".[dev]"

# Start PostgreSQL with AGE
docker-compose up -d postgres

# Run API server
uvicorn packages.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
# Navigate to UI package
cd packages/ui

# Install dependencies
npm install

# Start development server
npm run dev
```

## Database Schema

The database schema is automatically created when the PostgreSQL container starts. To manually recreate:

```bash
# Connect to database
docker exec -it keta-postgres psql -U postgres -d keta_db

# Check tables
\dt keta.*

# Check graph
SELECT * FROM ag_catalog.ag_graph;
```

## Usage

### 1. Create an Objective

```bash
curl -X POST http://localhost:8000/api/v1/objectives \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Company Analysis",
    "description": "Extract information about companies",
    "domain": "business"
  }'
```

### 2. Upload a Document

```bash
curl -X POST http://localhost:8000/api/v1/objectives/{objective_id}/sources \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Company Overview",
    "content": "Acme Corp was founded in 2020 by John Doe..."
  }'
```

### 3. Trigger Extraction

```bash
curl -X POST http://localhost:8000/api/v1/sources/{source_id}/extract
```

### 4. Create Chat Session

```bash
curl -X POST http://localhost:8000/api/v1/chat/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "objective_id": "{objective_id}",
    "name": "My Chat Session"
  }'
```

### 5. Send Message

```bash
curl -X POST http://localhost:8000/api/v1/chat/sessions/{session_id}/messages \
  -H "Content-Type: application/json" \
  -d '{
    "content": "What companies are mentioned?"
  }'
```


