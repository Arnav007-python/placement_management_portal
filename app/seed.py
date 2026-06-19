from . import db
from .models import CompanyProfile, Job, StudentProfile, User


def seed_database():
    db.drop_all()
    db.create_all()

    admin = User(name="Portal Admin", email="admin@portal.local", role="admin")
    admin.set_password("admin123")

    student_user = User(name="Aarav Sharma", email="student@portal.local", role="student")
    student_user.set_password("student123")
    student = StudentProfile(
        user=student_user,
        department="Computer Science",
        graduation_year=2026,
        cgpa=8.7,
        skills="Python, Flask, SQL, React",
    )

    company_user = User(name="Nisha Rao", email="hr@techcorp.local", role="company")
    company_user.set_password("company123")
    company = CompanyProfile(
        user=company_user,
        company_name="TechCorp Solutions",
        website="https://techcorp.example",
        industry="Software Services",
        approved=True,
    )

    jobs = [
        Job(
            company=company,
            title="Software Engineer Trainee",
            location="Bengaluru",
            package_lpa=7.5,
            min_cgpa=7.0,
            description="Build internal tools, APIs, and dashboards with a mentor-led engineering team.",
        ),
        Job(
            company=company,
            title="Data Analyst Intern",
            location="Hyderabad",
            package_lpa=4.2,
            min_cgpa=6.5,
            description="Analyze placement, product, and customer datasets using SQL and Python.",
        ),
    ]

    db.session.add_all([admin, student, company, *jobs])
    db.session.commit()
