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

### Windows

```powershell
.\start.ps1
```

Or double-click `start.bat`.

Then open `http://127.0.0.1:5000`.

To open the portal from another laptop or mobile phone, keep the server running and use the network URL printed by `start.ps1`, for example:

```text
http://192.168.1.10:5000
```

The other device must be connected to the same Wi-Fi/network. If Windows Firewall asks for permission, allow Python on private networks.

### Manual

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -c "from app import create_app; from app.bootstrap import ensure_admin_account; app=create_app(); ctx=app.app_context(); ctx.push(); ensure_admin_account()"
python run.py
```

Open `http://127.0.0.1:5000`.

For same-Wi-Fi mobile/laptop access, use your computer's IPv4 address:

```powershell
ipconfig
```

Then open:

```text
http://YOUR-IPV4-ADDRESS:5000
```

## Demo Accounts

After running `start.ps1` or the manual admin setup command:

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


