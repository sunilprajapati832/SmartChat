import smtplib
from email.message import EmailMessage
from config import Config
import requests  # For webhook

def send_lead_email(pdf_path):
    msg = EmailMessage()
    msg["Subject"] = "New Lead from UrbanNest AI"
    msg["From"] = Config.EMAIL_USERNAME
    msg["To"] = Config.ADMIN_EMAIL

    msg.set_content(
        "A new customer lead has been generated.\n"
        "Please find the attached chat history."
    )

    with open(pdf_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename=pdf_path
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(
            Config.EMAIL_USERNAME,
            Config.EMAIL_PASSWORD
        )
        server.send_message(msg)

def notify_webhook(webhook_url, data):
    if webhook_url:
        try:
            requests.post(webhook_url, json=data)
        except Exception as e:
            print(f"Webhook error: {e}")