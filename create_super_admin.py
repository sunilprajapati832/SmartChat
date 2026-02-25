from app import app, db
from models import SuperAdmin

with app.app_context():
    if not SuperAdmin.query.first():
        sa = SuperAdmin(username="admin")
        sa.set_password("admin123")
        db.session.add(sa)
        db.session.commit()
        print("✅ Super Admin Created")
    else:
        print("ℹ️ Super Admin Already Exists")
