from app import app, db
from models import Admin, Business
from werkzeug.security import generate_password_hash

with app.app_context():
    business = Business.query.filter_by(business_key="Urban_Nest").first()

    if not business:
        print("❌ Business not found")
        exit()

    admin = Admin(
        username="urban_admin",
        password=generate_password_hash("urban123"),
        business_id=business.id
    )

    db.session.add(admin)
    db.session.commit()

    print("✅ UrbanNest Admin Created Successfully")
