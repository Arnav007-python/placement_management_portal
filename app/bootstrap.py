from . import db
from .models import User


def ensure_admin_account():
    db.create_all()
    admin = User.query.filter_by(email="admin@portal.local").first()
    if admin is None:
        admin = User(name="Portal Admin", email="admin@portal.local", role="admin")
        admin.set_password("admin123")
        db.session.add(admin)
    else:
        admin.name = "Portal Admin"
        admin.role = "admin"
        admin.set_password("admin123")
    db.session.commit()
