from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from . import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    student_profile = db.relationship("StudentProfile", back_populates="user", uselist=False)
    company_profile = db.relationship("CompanyProfile", back_populates="user", uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class StudentProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True)
    department = db.Column(db.String(120), nullable=False)
    graduation_year = db.Column(db.Integer, nullable=False)
    cgpa = db.Column(db.Float, nullable=False)
    skills = db.Column(db.Text, default="")

    user = db.relationship("User", back_populates="student_profile")
    applications = db.relationship("Application", back_populates="student", cascade="all, delete-orphan")


class CompanyProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True)
    company_name = db.Column(db.String(160), nullable=False)
    website = db.Column(db.String(255), default="")
    industry = db.Column(db.String(120), nullable=False)
    approved = db.Column(db.Boolean, default=False, nullable=False)

    user = db.relationship("User", back_populates="company_profile")
    jobs = db.relationship("Job", back_populates="company", cascade="all, delete-orphan")


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company_profile.id"), nullable=False)
    title = db.Column(db.String(160), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    package_lpa = db.Column(db.Float, nullable=False)
    min_cgpa = db.Column(db.Float, nullable=False, default=0)
    description = db.Column(db.Text, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    company = db.relationship("CompanyProfile", back_populates="jobs")
    applications = db.relationship("Application", back_populates="job", cascade="all, delete-orphan")


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student_profile.id"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("job.id"), nullable=False)
    resume_filename = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(40), default="Applied", nullable=False)
    applied_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    student = db.relationship("StudentProfile", back_populates="applications")
    job = db.relationship("Job", back_populates="applications")

    __table_args__ = (db.UniqueConstraint("student_id", "job_id", name="unique_student_job"),)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
