# Claim POC

A FastAPI-based proof of concept for managing patient claims, insurance, and related data with PostgreSQL.

## Prerequisites

- Python 3.10+
- PostgreSQL 12+
- Git
- UV (Python package manager)

## Setup

1. **Clone the repository:**
   ```sh
   git clone <repository-url>
   cd claim-poc
   ```

2. **Set up Python environment with UV:**
   ```sh
   uv sync
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies (if not using UV sync):**
   ```sh
   uv pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database:**
   - Create a database: `claim_db`
   - Create a user: `claim_user` with password `password`
   - Grant permissions:
     ```sql
     CREATE DATABASE claim_db;
     CREATE USER claim_user WITH PASSWORD 'password';
     GRANT ALL PRIVILEGES ON DATABASE claim_db TO claim_user;
     GRANT ALL PRIVILEGES ON SCHEMA public TO claim_user;
     ```

5. **Configure environment variables:**
   - Copy `.env.example` to `.env` and update `DATABASE_URL` if needed.

6. **Run database migrations:**
   ```sh
   alembic upgrade head
   ```

7. **Run the application:**
   ```sh
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`. View docs at `http://localhost:8000/docs`.
