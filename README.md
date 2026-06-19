# Placement Management Portal

A complete final-year level placement portal built with Flask and SQLite.

## Features

- Student registration and login
- Company registration and login
- Job posting by companies
- Students can browse and apply for jobs
- Resume upload with application records
- Admin dashboard for students, companies, jobs, and applications
- SQLite persistence with seed data
- Pytest test suite and GitHub Actions CI

## Tech Stack

- Python 3.11+
- Flask
- Flask-Login
- Flask-SQLAlchemy
- SQLite
- Pytest

## Quick Start

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m flask --app app init-db
python -m flask --app app seed-db
python -m flask --app app run
```

Open `http://127.0.0.1:5000`.

## Demo Accounts

After running `seed-db`:

| Role | Email | Password |
| --- | --- | --- |
| Admin | admin@portal.local | admin123 |
| Student | student@portal.local | student123 |
| Company | hr@techcorp.local | company123 |

## Project Structure

```text
app/
  __init__.py
  auth.py
  company.py
  student.py
  admin.py
  models.py
  templates/
  static/
tests/
.github/workflows/ci.yml
```

## Environment Variables

| Variable | Default | Purpose |
| --- | --- | --- |
| `SECRET_KEY` | `dev-secret-key` | Flask session signing key |
| `DATABASE_URL` | `sqlite:///placement_portal.db` | SQLAlchemy database URL |
| `UPLOAD_FOLDER` | `uploads/resumes` | Resume storage directory |

## Notes

Uploaded resumes are stored under `uploads/resumes` by default. The directory is ignored by Git to avoid committing student documents.
