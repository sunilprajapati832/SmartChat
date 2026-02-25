from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
IST = pytz.timezone("Asia/Kolkata")

# ---------------- SUPER ADMIN ----------------
class SuperAdmin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# ---------------- BUSINESS ----------------
class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    business_key = db.Column(db.String(50), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    subscription_start = db.Column(db.DateTime)  # New
    subscription_end = db.Column(db.DateTime)  # New
    webhook_url = db.Column(db.String(255))  # New


# ---------------- BUSINESS ADMIN ----------------
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    business_id = db.Column(
        db.Integer,
        db.ForeignKey("business.id"),
        nullable=False
    )

    business = db.relationship("Business", backref="admins")



# ---------------- LEADS ----------------
class Lead(db.Model):
    __tablename__ = "lead"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100))

    # ✅ APP USES business_key → KEEP IT
    business_key = db.Column(db.String(100), index=True)

    status = db.Column(db.String(20), default="New")
    priority = db.Column(db.String(20), default="Warm")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def ist_created_at(self):
        try:
            utc_time = pytz.utc.localize(self.created_at)
            return utc_time.astimezone(IST)
        except Exception:
            return self.created_at

# ---------------- CHAT MESSAGES ----------------
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey("lead.id"))
    sender = db.Column(db.String(20))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def ist_timestamp(self):
        try:
            utc_time = pytz.utc.localize(self.timestamp)
            return utc_time.astimezone(IST)
        except Exception:
            return self.timestamp

# ---------------- QnA ----------------
class QnA(db.Model):
    __tablename__ = "qna"

    id = db.Column(db.Integer, primary_key=True)

    # ✅ REQUIRED BY app.py
    business_key = db.Column(db.String(100), index=True)

    keyword = db.Column(db.String(100))
    reply = db.Column(db.Text)

    __table_args__ = (
        db.UniqueConstraint("business_key", "keyword"),
    )


# ---------------- BUSINESS SETTINGS ----------------
class BusinessSettings(db.Model):
    __tablename__ = "business_settings"

    id = db.Column(db.Integer, primary_key=True)

    # ✅ THIS FIXES YOUR ERROR
    business_key = db.Column(db.String(100), unique=True, nullable=False)

    brand_name = db.Column(db.String(100), default="SmartChat")
    greeting_text = db.Column(db.String(255), default="Hi! How can I help you?")

    primary_color = db.Column(db.String(20), default="#0072ff")
    background_color = db.Column(db.String(20), default="#ffffff")
    admin_theme_color = db.Column(db.String(20), default="#1a73e8")

    font_family = db.Column(db.String(50), default="Inter, Arial")

    dark_mode = db.Column(db.Boolean, default=True)
    transparent_chat = db.Column(db.Boolean, default=True)

    chat_position = db.Column(db.String(10), default="right")
    logo_url = db.Column(db.String(255))