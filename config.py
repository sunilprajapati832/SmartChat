import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # --------------------------------------------------
    # CORE SECURITY
    # --------------------------------------------------
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")

    # --------------------------------------------------
    # DATABASE CONFIG
    # --------------------------------------------------
    DATABASE_URL = os.getenv("DATABASE_URL")

    if DATABASE_URL:
        # Render / Production (PostgreSQL)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace(
            "postgres://", "postgresql://", 1
        )
    else:
        # Local development (SQLite)
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
            BASE_DIR, "instance", "chat.db"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --------------------------------------------------
    # EMAIL CONFIG (SMTP)
    # --------------------------------------------------
    ADMIN_EMAIL = os.getenv("SUPER_ADMIN_EMAIL", "sunilp832@gmail.com")

    EMAIL_USERNAME = os.getenv("SMTP_EMAIL", "sunilp832@gmail.com")
    EMAIL_PASSWORD = os.getenv("SMTP_PASSWORD", "cmmn ekie izcx twwr")

    # --------------------------------------------------
    # OPENAI (OPTIONAL)
    # --------------------------------------------------
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")