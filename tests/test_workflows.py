from app.models import Application, CompanyProfile, Job
from app import db

from conftest import login, resume_file


def test_student_can_apply_with_resume(client, app):
    login(client, "student@test.local")
    response = client.post(
        "/student/jobs/1/apply",
        data={"resume": resume_file()},
        content_type="multipart/form-data",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Application submitted successfully" in response.data
    with app.app_context():
        assert Application.query.count() == 1


def test_company_can_post_job_when_approved(client, app):
    login(client, "company@test.local")
    response = client.post(
        "/company/jobs/new",
        data={
            "title": "QA Engineer",
            "location": "Pune",
            "package_lpa": "5.5",
            "min_cgpa": "6.5",
            "description": "Test web applications.",
            "active": "on",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    with app.app_context():
        assert Job.query.filter_by(title="QA Engineer").first() is not None


def test_pending_company_cannot_post_job(client, app):
    with app.app_context():
        pending_user = CompanyProfile.query.first().user
        pending_user.email = "pending@test.local"
        pending_user.company_profile.approved = False
        db.session.commit()

    login(client, "pending@test.local")
    response = client.get("/company/jobs/new", follow_redirects=True)

    assert b"Admin approval is required" in response.data


def test_admin_can_approve_company(client, app):
    with app.app_context():
        company_id = CompanyProfile.query.first().id

    login(client, "admin@test.local")
    response = client.post(
        f"/admin/companies/{company_id}/approval",
        data={"approved": "false"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    with app.app_context():
        assert db.session.get(CompanyProfile, company_id).approved is False
