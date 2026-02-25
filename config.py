import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "super-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "instance", "chat.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ADMIN_EMAIL = "sunilp832@gmail.com"
    EMAIL_USERNAME = "sunilp832@gmail.com"
    EMAIL_PASSWORD = "cmmn ekie izcx twwr"
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")  # Set your OpenAI key here or in env