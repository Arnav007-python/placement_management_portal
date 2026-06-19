from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from . import db
from .models import CompanyProfile, StudentProfile, User

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Welcome back.", "success")
            return redirect(url_for("index"))
        flash("Invalid email or password.", "danger")

    return render_template("auth/login.html")


@bp.route("/register/student", methods=["GET", "POST"])
def register_student():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        if User.query.filter_by(email=email).first():
            flash("An account with this email already exists.", "danger")
            return redirect(url_for("auth.register_student"))

        user = User(name=request.form["name"].strip(), email=email, role="student")
        user.set_password(request.form["password"])
        profile = StudentProfile(
            user=user,
            department=request.form["department"].strip(),
            graduation_year=int(request.form["graduation_year"]),
            cgpa=float(request.form["cgpa"]),
            skills=request.form.get("skills", "").strip(),
        )
        db.session.add(profile)
        db.session.commit()
        flash("Student account created. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register_student.html")


@bp.route("/register/company", methods=["GET", "POST"])
def register_company():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        if User.query.filter_by(email=email).first():
            flash("An account with this email already exists.", "danger")
            return redirect(url_for("auth.register_company"))

        user = User(name=request.form["contact_name"].strip(), email=email, role="company")
        user.set_password(request.form["password"])
        profile = CompanyProfile(
            user=user,
            company_name=request.form["company_name"].strip(),
            website=request.form.get("website", "").strip(),
            industry=request.form["industry"].strip(),
            approved=False,
        )
        db.session.add(profile)
        db.session.commit()
        flash("Company account submitted. Admin approval is required before posting jobs.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register_company.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
