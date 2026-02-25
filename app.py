import gevent
from gevent import monkey
monkey.patch_all()

from functools import wraps
from datetime import datetime, timedelta
import uuid

from flask import (
    Flask, render_template, session, request,
    redirect, url_for, flash
)
from flask_socketio import SocketIO, emit
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import or_, func
from sqlalchemy.exc import IntegrityError

from config import Config
from models import (
    db, Lead, Message, QnA,
    Admin, SuperAdmin, Business,
    BusinessSettings
)
from services.pdf_service import generate_lead_pdf
from services.email_service import send_lead_email, notify_webhook  # Updated import
from services.chat_engine import get_reply  # Use updated get_reply

# ======================================================
# APP SETUP
# ======================================================

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config.get("SECRET_KEY", "smartchat-secret")

db.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="gevent")  # Changed to gevent

with app.app_context():
    db.create_all()

# ======================================================
# PUBLIC
# ======================================================

@app.route("/")
def home():
    return redirect("/widget?business=demo_business")

@app.route("/widget")
def widget():
    business_key = request.args.get("business", "demo_business")
    session["business_key"] = business_key

    business = Business.query.filter_by(
        business_key=business_key,
        is_active=True
    ).first()

    if not business:
        return "❌ Business not active", 403

    # Check subscription
    if business.subscription_end and business.subscription_end < datetime.utcnow():
        return "❌ Subscription expired", 403

    settings = BusinessSettings.query.filter_by(
        business_key=business_key
    ).first()

    if not settings:
        settings = BusinessSettings(business_key=business_key)
        db.session.add(settings)
        db.session.commit()

    if "lead_id" not in session:
        lead = Lead(
            session_id=str(uuid.uuid4()),
            business_key=business_key
        )
        db.session.add(lead)
        db.session.commit()
        session["lead_id"] = lead.id
        notify_webhook(business.webhook_url, {"event": "new_lead", "lead_id": lead.id})  # New webhook call

    return render_template("chat_widget.html", settings=settings)


# ======================================================
# SOCKET CHAT
# ======================================================

@socketio.on("user_message")
def handle_user_message(data):
    message = data.get("message", "").strip().lower()
    lead_id = session.get("lead_id")
    business_key = session.get("business_key")

    if not message or not lead_id or not business_key:
        return

    db.session.add(Message(
        lead_id=lead_id,
        sender="visitor",
        content=message
    ))
    db.session.commit()

    reply = get_reply(message, business_key)  # Updated to pass business_key for QnA filter

    db.session.add(Message(
        lead_id=lead_id,
        sender="bot",
        content=reply
    ))
    db.session.commit()

    emit("bot_reply", {"message": reply})


# ======================================================
# SUPER ADMIN
# ======================================================

@app.route("/sa/login", methods=["GET", "POST"])
def super_admin_login():
    if request.method == "POST":
        admin = SuperAdmin.query.filter_by(
            username=request.form["username"]
        ).first()

        if admin and admin.check_password(request.form["password"]):
            session.clear()
            session["super_admin"] = True
            return redirect("/sa/dashboard")

    return render_template("sa_login.html")


@app.route("/sa/dashboard")
def super_admin_dashboard():
    if not session.get("super_admin"):
        return redirect("/sa/login")

    businesses = Business.query.order_by(
        Business.created_at.desc()
    ).all()

    business_details = []
    for b in businesses:
        admins = Admin.query.filter_by(business_id=b.id).all()
        business_details.append({
            'business': b,
            'admins': [a.username for a in admins],
            'is_expired': b.subscription_end < datetime.utcnow() if b.subscription_end else False
        })

    return render_template("sa_dashboard.html", businesses=business_details)


@app.route("/sa/create-business", methods=["POST"])
def create_business():
    if not session.get("super_admin"):
        return redirect("/sa/login")

    business = Business(
        name=request.form["name"],
        business_key=request.form["business_key"],
        subscription_start=datetime.utcnow(),
        subscription_end=datetime.utcnow() + timedelta(days=30),  # 30-day trial
        webhook_url=request.form.get("webhook_url", "")
    )
    db.session.add(business)
    db.session.commit()

    return redirect("/sa/dashboard")

@app.route("/sa/edit-business/<int:business_id>", methods=["GET", "POST"])
def edit_business(business_id):
    if not session.get("super_admin"):
        return redirect("/sa/login")

    business = Business.query.get_or_404(business_id)

    if request.method == "POST":
        business.name = request.form["name"]
        business.is_active = "is_active" in request.form
        business.subscription_end = datetime.strptime(request.form["subscription_end"], "%Y-%m-%d")
        business.webhook_url = request.form["webhook_url"]
        db.session.commit()
        flash("Business updated", "success")
        return redirect("/sa/dashboard")

    return render_template("sa_edit_business.html", business=business)

@app.route("/sa/renew-business/<int:business_id>", methods=["POST"])
def renew_business(business_id):
    if not session.get("super_admin"):
        return redirect("/sa/login")

    business = Business.query.get_or_404(business_id)
    business.subscription_end = datetime.utcnow() + timedelta(days=30)
    db.session.commit()
    flash("Subscription renewed", "success")
    return redirect("/sa/dashboard")

@app.route("/sa/delete-business/<int:business_id>", methods=["POST"])
def delete_business(business_id):
    if not session.get("super_admin"):
        return redirect("/sa/login")

    business = Business.query.get_or_404(business_id)
    db.session.delete(business)
    db.session.commit()
    flash("Business deleted", "success")
    return redirect("/sa/dashboard")

@app.route("/sa/activate-business/<int:business_id>")
def activate_business(business_id):
    if not session.get("super_admin"):
        return redirect("/sa/login")

    business = Business.query.get_or_404(business_id)
    business.is_active = True
    db.session.commit()
    return redirect("/sa/dashboard")

@app.route("/sa/profile", methods=["GET", "POST"])
def super_admin_profile():
    if not session.get("super_admin"):
        return redirect("/sa/login")

    if request.method == "POST":
        if "change_password" in request.form:
            sa = SuperAdmin.query.first()
            old_password = request.form["old_password"]
            new_password = request.form["new_password"]
            if sa and sa.check_password(old_password):
                sa.set_password(new_password)
                db.session.commit()
                flash("Password changed successfully", "success")
            else:
                flash("Invalid old password", "danger")

        return redirect("/sa/profile")

    return render_template("sa_profile.html")

@app.route("/sa/logout")
def super_admin_logout():
    session.clear()
    return redirect("/sa/login")

@app.route("/sa/change-admin-password/<int:admin_id>", methods=["POST"])
def change_admin_password(admin_id):
    if not session.get("super_admin"):
        return redirect("/sa/login")

    admin = Admin.query.get_or_404(admin_id)
    new_password = request.form["new_admin_password"]

    admin.password = generate_password_hash(new_password)
    db.session.commit()
    flash(f"Password changed for admin {admin.username}", "success")

    return redirect("/sa/dashboard")

# ======================================================
# ADMIN AUTH
# ======================================================

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect("/admin/login")
        return f(*args, **kwargs)
    return wrapper


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        admin = Admin.query.filter_by(
            username=request.form.get("username")
        ).first()

        if admin and check_password_hash(
            admin.password,
            request.form.get("password")
        ):
            session["admin_logged_in"] = True
            session["business_key"] = admin.business.business_key
            return redirect("/admin")

        flash("Invalid credentials", "danger")

    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect("/admin/login")


# ======================================================
# ADMIN DASHBOARD
# ======================================================

@app.route("/admin")
@admin_required
def admin_dashboard():
    business_key = session["business_key"]
    search = request.args.get("search", "").strip().lower()

    leads_query = (
        Lead.query
        .filter_by(business_key=business_key)
        .outerjoin(Message)
    )

    if search:
        conditions = [
            Lead.session_id.ilike(f"%{search}%"),
            Message.content.ilike(f"%{search}%"),
            Lead.status.ilike(search),
            Lead.priority.ilike(search)
        ]

        if search.isdigit():
            conditions.append(Lead.id == int(search))

        try:
            dt = datetime.strptime(search, "%d-%m-%Y")
            conditions.append(
                Lead.created_at.between(dt, dt + timedelta(days=1))
            )
        except:
            pass

        leads_query = leads_query.filter(or_(*conditions))

    leads = leads_query.distinct().order_by(
        Lead.created_at.desc()
    ).all()

    analytics = {
        "total": Lead.query.filter_by(business_key=business_key).count(),
        "new": Lead.query.filter_by(business_key=business_key, status="New").count(),
        "contacted": Lead.query.filter_by(business_key=business_key, status="Contacted").count(),
        "closed": Lead.query.filter_by(business_key=business_key, status="Closed").count(),
    }

    settings = BusinessSettings.query.filter_by(
        business_key=business_key
    ).first()

    return render_template(
        "admin_dashboard.html",
        leads=leads,
        analytics=analytics,
        search=search,
        settings=settings
    )

# ======================================================
# UPDATE STATUS / PRIORITY
# ======================================================

@app.route("/admin/lead/<int:lead_id>/status", methods=["POST"])
@admin_required
def update_status(lead_id):
    lead = Lead.query.get_or_404(lead_id)
    lead.status = request.form.get("status")
    db.session.commit()
    return redirect("/admin")

@app.route("/admin/lead/<int:lead_id>/priority", methods=["POST"])
@admin_required
def update_priority(lead_id):
    lead = Lead.query.get_or_404(lead_id)
    lead.priority = request.form.get("priority")
    db.session.commit()
    return redirect("/admin")

# ======================================================
# VIEW CHAT
# ======================================================

@app.route("/admin/lead/<int:lead_id>")
@admin_required
def view_chat(lead_id):
    business_key = session.get("business_key", "demo_business")

    lead = Lead.query.filter_by(
        id=lead_id,
        business_key=business_key
    ).first_or_404()

    messages = (
        Message.query
        .filter_by(lead_id=lead.id)
        .order_by(Message.timestamp)
        .all()
    )

    return render_template(
        "admin_chat_timeline.html",
        lead=lead,
        messages=messages
    )

# ======================================================
# ANALYTICS (FIXED – NO MORE 404)
# ======================================================

@app.route("/admin/analytics")
@admin_required
def admin_analytics():
    business_key = session.get("business_key", "demo_business")

    total = Lead.query.filter_by(business_key=business_key).count()
    new = Lead.query.filter_by(business_key=business_key, status="New").count()
    contacted = Lead.query.filter_by(business_key=business_key, status="Contacted").count()
    closed = Lead.query.filter_by(business_key=business_key, status="Closed").count()

    # 🔴 IMPORTANT FIX: provide chart-safe data
    daily = (
        db.session.query(
            func.date(Lead.created_at),
            func.count(Lead.id)
        )
        .filter(Lead.business_key == business_key)
        .group_by(func.date(Lead.created_at))
        .order_by(func.date(Lead.created_at))
        .all()
    )

    dates = [str(row[0]) for row in daily]
    counts = [row[1] for row in daily]

    return render_template(
        "admin_analytics.html",
        analytics={
            "total": total,
            "new": new,
            "contacted": contacted,
            "closed": closed
        },
        dates=dates,
        counts=counts
    )


# ======================================================
# QNA + EXPORT (UNCHANGED)
# ======================================================

@app.route("/admin/qna", methods=["GET", "POST"])
@admin_required
def qna():
    business_key = session["business_key"]

    if request.method == "POST":
        keyword = request.form["keyword"].strip().lower()
        reply = request.form["reply"].strip()

        try:
            q = QnA(
                business_key=business_key,
                keyword=keyword,
                reply=reply
            )
            db.session.add(q)
            db.session.commit()
            flash("Q&A added", "success")
        except IntegrityError:
            db.session.rollback()
            flash("Keyword already exists", "warning")

        return redirect(url_for("qna"))

    qna_list = QnA.query.filter_by(
        business_key=business_key
    ).all()

    return render_template("admin_qna.html", qna_list=qna_list)

@app.route("/admin/qna/suggestions")
@admin_required
def qna_suggestions():
    suggestions = (
        db.session.query(
            Message.content,
            func.count(Message.content).label("count")
        )
        .filter(Message.sender == "visitor")
        .group_by(Message.content)
        .having(func.count(Message.content) >= 2)
        .order_by(func.count(Message.content).desc())
        .all()
    )

    return render_template(
        "admin_qna_suggestions.html",
        suggestions=suggestions
    )

@app.route("/admin/qna/delete/<int:id>", methods=["POST"])
@admin_required
def delete_qna(id):
    qna = QnA.query.get_or_404(id)
    db.session.delete(qna)
    db.session.commit()
    flash("Deleted", "success")
    return redirect(url_for("qna"))

@app.route("/admin/export/<int:lead_id>")
@admin_required
def export_lead(lead_id):
    lead = Lead.query.get_or_404(lead_id)
    messages = Message.query.filter_by(lead_id=lead_id).all()

    pdf_path = generate_lead_pdf(lead, messages)
    send_lead_email(pdf_path)

    return "✅ Lead exported and emailed"


# ======================================================
# ADMIN SETTING
# ======================================================

@app.route("/admin/settings", methods=["GET","POST"])
@admin_required
def admin_settings():
    business_key = session.get("business_key", "demo_business")

    s = BusinessSettings.query.filter_by(
        business_key=business_key
    ).first()

    if request.method == "POST":
        s.brand_name = request.form["brand_name"]
        s.greeting_text = request.form["greeting_text"]
        s.primary_color = request.form["primary_color"]
        s.font_family = request.form["font_family"]
        s.chat_position = request.form["chat_position"]
        s.dark_mode = "dark_mode" in request.form
        s.transparent_chat = "transparent_chat" in request.form
        db.session.commit()

    return render_template("admin_settings.html", s=s)

# ======================================================
# RUN
# ======================================================

if __name__ == "__main__":
    socketio.run(app, host="127.0.0.1", port=5000, debug=True)