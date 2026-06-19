import io

import pytest

from app import create_app, db
from app.models import CompanyProfile, Job, StudentProfile, User


@pytest.fixture()
def app(tmp_path):
    test_app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,
            "UPLOAD_FOLDER": str(tmp_path / "uploads"),
        }
    )
    with test_app.app_context():
        db.create_all()
        seed_core_data()
        yield test_app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def seed_core_data():
    admin = User(name="Admin", email="admin@test.local", role="admin")
    admin.set_password("password")

    student_user = User(name="Student", email="student@test.local", role="student")
    student_user.set_password("password")
    student = StudentProfile(
        user=student_user,
        department="CSE",
        graduation_year=2026,
        cgpa=8.5,
        skills="Python",
    )

    company_user = User(name="HR", email="company@test.local", role="company")
    company_user.set_password("password")
    company = CompanyProfile(
        user=company_user,
        company_name="Acme",
        industry="IT",
        approved=True,
    )
    job = Job(
        company=company,
        title="Developer",
        location="Remote",
        package_lpa=6.0,
        min_cgpa=7.0,
        description="Build web apps.",
    )

    db.session.add_all([admin, student, company, job])
    db.session.commit()


def login(client, email, password="password"):
    return client.post("/login", data={"email": email, "password": password}, follow_redirects=True)


def resume_file(name="resume.pdf"):
    return io.BytesIO(b"%PDF-1.4 test resume"), name
