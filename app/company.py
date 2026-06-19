from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from . import db
from .decorators import role_required
from .models import Application, Job

bp = Blueprint("company", __name__, url_prefix="/company")


@bp.route("/dashboard")
@login_required
@role_required("company")
def dashboard():
    company = current_user.company_profile
    jobs = Job.query.filter_by(company=company).order_by(Job.created_at.desc()).all()
    applications = (
        Application.query.join(Job)
        .filter(Job.company_id == company.id)
        .order_by(Application.applied_at.desc())
        .all()
    )
    return render_template("company/dashboard.html", company=company, jobs=jobs, applications=applications)


@bp.route("/jobs/new", methods=["GET", "POST"])
@login_required
@role_required("company")
def new_job():
    company = current_user.company_profile
    if not company.approved:
        flash("Admin approval is required before posting jobs.", "warning")
        return redirect(url_for("company.dashboard"))

    if request.method == "POST":
        job = Job(
            company=company,
            title=request.form["title"].strip(),
            location=request.form["location"].strip(),
            package_lpa=float(request.form["package_lpa"]),
            min_cgpa=float(request.form["min_cgpa"]),
            description=request.form["description"].strip(),
            active=bool(request.form.get("active")),
        )
        db.session.add(job)
        db.session.commit()
        flash("Job posted successfully.", "success")
        return redirect(url_for("company.dashboard"))

    return render_template("company/job_form.html")


@bp.route("/applications/<int:application_id>/status", methods=["POST"])
@login_required
@role_required("company")
def update_application_status(application_id):
    application = db.get_or_404(Application, application_id)
    if application.job.company_id != current_user.company_profile.id:
        flash("You cannot update another company's application.", "danger")
        return redirect(url_for("company.dashboard"))
    application.status = request.form["status"]
    db.session.commit()
    flash("Application status updated.", "success")
    return redirect(url_for("company.dashboard"))
