# 🤖 SmartChat – Multi-Business AI Chatbox Platform

SmartChat is a plug-and-play, **multi-tenant AI chatbox system** designed for **any type of business website**, such as:

- 🏢 Real Estate  
- 🏬 E-commerce  
- 🏥 Clinics  
- 🏫 Education  
- 🏨 Hotels  
- 🧑‍💼 Service-based businesses  

**UrbanNest** is used only as a **demo / example business** to showcase SmartChat’s real-world implementation.

---

## 🌐 What SmartChat Does

SmartChat can be embedded into any business website to:

- Automatically answer customer queries  
- Capture and manage leads  
- Export chat conversations as PDF  
- Email leads to the **respective business admin**  
- Maintain separate data, branding, and settings per business  

This makes **SmartChat a SaaS-ready product**, not a single-website chatbot.

---

## ✨ Core Features

### 🧠 AI Chat Widget
- Floating AI chat button  
- Draggable chat widget & AI icon  
- Business-specific greetings  
- Keyword-based automated replies  
- Typing indicator & real-time chat  

### 🏢 Multi-Business (SaaS Architecture)
- Unlimited businesses  
- Each business has:
  - Unique `business_key`
  - Separate chats, leads & QnA
  - Custom branding & settings  
- One codebase → many businesses  

### 👤 Role-Based Access

#### 🔑 Super Admin
- View & manage all businesses  
- Add & manage:
  - Business email  
  - Security key  
  - Business website  
- Monitor global leads & analytics  

#### 🧑‍💼 Business Admin
- Login to own dashboard  
- Manage QnA keywords  
- View chat history & leads  
- Receive chat PDFs via email  
- Customize chat appearance  

---

## 📄 Lead & PDF Automation
- Each chat session creates a **Lead**  
- Messages stored securely in database  
- Chat history exported as **Unicode-safe PDF**  
- PDF automatically emailed to the **business admin**  
- Optional webhook notifications supported  

---

## 🖼️ Screenshots (UrbanNest Demo)

![SmartChat Widget](screenshots/chat_widget.png)
![Business Admin Dashboard](screenshots/admin_dashboard.png)
![Chat Conversation PDF](screenshots/chat_pdf.png)

> Screenshots are from the UrbanNest demo, but SmartChat works identically for **any business**.

---

## 🛠️ Tech Stack

### Backend
- Python (Flask)  
- Flask-SQLAlchemy  
- Flask-SocketIO  

### Frontend
- HTML, CSS, JavaScript  
- Glassmorphism UI  
- Drag & drop interactions  

### Database
- SQLite (Development)  
- PostgreSQL (Production)  

### Other
- ReportLab (PDF generation)  
- SMTP Email  
- Webhooks  
- Git & GitHub  

---

## 📁 Project Structure
SmartChat/
│── app.py
│── config.py
│── models.py
│── requirements.txt
│
├── services/
│ ├── chat_engine.py
│ ├── email_service.py
│ ├── pdf_service.py
│
├── static/
│ ├── chat.css
│ ├── chat.js
│ ├── widget_loader.js
│
├── templates/
│ ├── chat_widget.html
│ ├── admin_dashboard.html
│ └── ...
│
└── leads/
└── lead_1.pdf


---

## ⚙️ Setup Instructions

```bash
git clone https://github.com/YOUR_USERNAME/smartchat.git
cd smartchat
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py

🔐 Business Configuration Flow

Each business provides:

📧 Business Email (for lead PDFs)

🔑 Security Key

🌍 Business Website URL

These are:

Managed by Super Admin

Used for email + webhook delivery

Fully isolated per business

🚀 Production Ready

SmartChat is ready for:

SaaS deployment

Subscription-based model

Multiple clients

Cloud hosting (Render, Railway, VPS, AWS)

👨‍💻 Author

Sunil Prajapati
Data Analyst | AI/ML Researcher

Project: SmartChat – Multi-Business AI Chat Platform

⭐ Support

If this project helps you, please ⭐ star the repository.
