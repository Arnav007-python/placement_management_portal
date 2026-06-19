from pathlib import Path

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

from . import db
from .decorators import role_required
from .models import Application, Job

bp = Blueprint("student", __name__, url_prefix="/student")

ALLOWED_RESUME_EXTENSIONS = {"pdf", "doc", "docx"}


def allowed_resume(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_RESUME_EXTENSIONS


@bp.route("/dashboard")
@login_required
@role_required("student")
def dashboard():
    profile = current_user.student_profile
    jobs = Job.query.filter_by(active=True).order_by(Job.created_at.desc()).all()
    applications = Application.query.filter_by(student=profile).all()
    applied_job_ids = {application.job_id for application in applications}
    return render_template(
        "student/dashboard.html",
        profile=profile,
        jobs=jobs,
        applications=applications,
        applied_job_ids=applied_job_ids,
    )


@bp.route("/jobs/<int:job_id>/apply", methods=["POST"])
@login_required
@role_required("student")
def apply(job_id):
    job = db.get_or_404(Job, job_id)
    resume = request.files.get("resume")
    if not resume or resume.filename == "":
        flash("Please upload a resume.", "danger")
        return redirect(url_for("student.dashboard"))
    if not allowed_resume(resume.filename):
        flash("Resume must be a PDF, DOC, or DOCX file.", "danger")
        return redirect(url_for("student.dashboard"))

    safe_name = secure_filename(resume.filename)
    filename = f"student-{current_user.id}-job-{job.id}-{safe_name}"
    upload_path = Path(current_app.config["UPLOAD_FOLDER"]) / filename
    resume.save(upload_path)

    application = Application(
        student=current_user.student_profile,
        job=job,
        resume_filename=filename,
    )
    db.session.add(application)
    try:
        db.session.commit()
        flash("Application submitted successfully.", "success")
    except IntegrityError:
        db.session.rollback()
        upload_path.unlink(missing_ok=True)
        flash("You have already applied for this job.", "warning")
    return redirect(url_for("student.dashboard"))
