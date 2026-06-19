from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from . import db
from .decorators import role_required
from .models import Application, CompanyProfile, Job, StudentProfile, User

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/dashboard")
@login_required
@role_required("admin")
def dashboard():
    stats = {
        "students": StudentProfile.query.count(),
        "companies": CompanyProfile.query.count(),
        "jobs": Job.query.count(),
        "applications": Application.query.count(),
    }
    companies = CompanyProfile.query.order_by(CompanyProfile.approved.asc(), CompanyProfile.company_name).all()
    jobs = Job.query.order_by(Job.created_at.desc()).all()
    applications = Application.query.order_by(Application.applied_at.desc()).all()
    students = StudentProfile.query.join(User).order_by(User.name).all()
    return render_template(
        "admin/dashboard.html",
        stats=stats,
        companies=companies,
        jobs=jobs,
        applications=applications,
        students=students,
    )


@bp.route("/companies/<int:company_id>/approval", methods=["POST"])
@login_required
@role_required("admin")
def approval(company_id):
    company = db.get_or_404(CompanyProfile, company_id)
    company.approved = request.form["approved"] == "true"
    db.session.commit()
    flash("Company approval updated.", "success")
    return redirect(url_for("admin.dashboard"))


@bp.route("/jobs/<int:job_id>/toggle", methods=["POST"])
@login_required
@role_required("admin")
def toggle_job(job_id):
    job = db.get_or_404(Job, job_id)
    job.active = not job.active
    db.session.commit()
    flash("Job status updated.", "success")
    return redirect(url_for("admin.dashboard"))
