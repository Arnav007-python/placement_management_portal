from pathlib import Path

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev-secret-key",
        SQLALCHEMY_DATABASE_URI="sqlite:///placement_portal.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        UPLOAD_FOLDER=str(Path("uploads") / "resumes"),
        MAX_CONTENT_LENGTH=4 * 1024 * 1024,
    )

    if test_config:
        app.config.update(test_config)

    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

    from . import admin, auth, company, student

    app.register_blueprint(auth.bp)
    app.register_blueprint(student.bp)
    app.register_blueprint(company.bp)
    app.register_blueprint(admin.bp)

    @app.route("/")
    def index():
        from flask import redirect, url_for
        from flask_login import current_user

        if current_user.is_authenticated:
            if current_user.role == "admin":
                return redirect(url_for("admin.dashboard"))
            if current_user.role == "company":
                return redirect(url_for("company.dashboard"))
            return redirect(url_for("student.dashboard"))
        return redirect(url_for("auth.login"))

    @app.cli.command("init-db")
    def init_db_command():
        with app.app_context():
            db.drop_all()
            db.create_all()
        print("Initialized the database.")

    @app.cli.command("seed-db")
    def seed_db_command():
        from .seed import seed_database

        with app.app_context():
            seed_database()
        print("Seeded demo data.")

    return app
