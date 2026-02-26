import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "instance", "chat.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

    EMAIL_USERNAME = os.environ.get("SMTP_EMAIL")
    EMAIL_PASSWORD = os.environ.get("SMTP_PASSWORD")

    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")