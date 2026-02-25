from models import QnA
from config import Config
import openai

def get_reply(user_message, business_key):
    msg = user_message.lower()
    msg_words = msg.split()  # Split message into words for better matching

    qnas = QnA.query.filter_by(business_key=business_key).all()
    for qna in qnas:
        # Split keyword by commas to handle multiple keywords (e.g., "budget, under, affordable")
        keywords = [k.strip().lower() for k in qna.keyword.split(',') if k.strip()]
        for keyword_lower in keywords:
            # Check if keyword is in message or any word matches keyword
            if keyword_lower in msg or any(word == keyword_lower for word in msg_words):
                return qna.reply

    # AI Fallback (skipped if no key)
    if Config.OPENAI_API_KEY:
        openai.api_key = Config.OPENAI_API_KEY
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": msg}]
            )
            return response.choices[0].message['content']
        except Exception as e:
            print(f"AI error: {e}")

    # Default fallback
    return (
        "Thanks for reaching out 😊\n"
        "SmartChat has shared your query with our team.\n"
        "We’ll contact you shortly."
    )