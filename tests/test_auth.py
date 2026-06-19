from app.models import CompanyProfile, StudentProfile, User


def test_login_redirects_student_to_dashboard(client):
    response = client.post(
        "/login",
        data={"email": "student@test.local", "password": "password"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Available Jobs" in response.data


def test_register_student_creates_profile(client, app):
    response = client.post(
        "/register/student",
        data={
            "name": "New Student",
            "email": "new@student.local",
            "password": "secret123",
            "department": "ECE",
            "graduation_year": "2026",
            "cgpa": "8.2",
            "skills": "Java, SQL",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    with app.app_context():
        assert StudentProfile.query.join(User).filter(User.email == "new@student.local").first()


def test_register_company_starts_pending(client, app):
    client.post(
        "/register/company",
        data={
            "company_name": "Future Labs",
            "contact_name": "Recruiter",
            "email": "hr@future.local",
            "password": "secret123",
            "industry": "Research",
            "website": "https://future.example",
        },
    )

    with app.app_context():
        company = CompanyProfile.query.filter_by(company_name="Future Labs").first()
        assert company is not None
        assert company.approved is False
