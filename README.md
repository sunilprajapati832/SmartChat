# 🤖 SmartChat – Multi-Business AI Chatbox SaaS Platform
SmartChat is a plug-and-play, **multi-tenant AI chatbox system** designed for **any type of business website**, such as:
- 🏢 Real Estate  
- 🏬 E-commerce  
- 🏥 Clinics  
- 🏫 Education  
- 🏨 Hotels  
- 🧑‍💼 Service-based businesses  
**UrbanNest** is used only as a **demo / example business** to showcase SmartChat’s real-world implementation.
Built with scalability in mind, SmartChat allows multiple businesses to operate independently from a single codebase, making it ideal for SaaS deployment.

## 🌟 The Story Behind SmartChat

SmartChat was born from a real-world problem. While developing UrbanNest, a real estate platform where users can buy, sell and rent properties seamlessly, one major challenge became evident: 
When customers had questions — technical or business-related — they had to wait for an admin response. 
This delay negatively impacted user experience. I explored existing chat solutions in the market and observed:
Most real-time chat services are paid.
- Subscription costs are high.
- Technical integration is complex.
- Ongoing support requires additional expenses.
- Non-technical business owners struggle with configuration.

That’s when the idea emerged: What if businesses could have a plug-and-play AI chat system that:
- Works like a simple plugin
- Requires minimal changes to an existing website
- Allows business owners to manage their own Q&A
- Captures leads automatically

Feels like a real customer care system. SmartChat was created to solve this problem. It is not just a chatbot — it is a self-managed, multi-business AI communication platform. Although still under active development, the core system is fully operational, including:
- Super Admin
- Business Admin
- Multi-business architecture
- Real-time chat engine
- Lead capture
- PDF automation
- Email notifications
The remaining work focuses on seamless website embedding and advanced integrations.

## 🧠 What SmartChat Does
SmartChat can be embedded into any business website to:
- Automatically answer customer queries (According to Admin Keyword Given in QnA Section) 
- Capture and manage leads  
- Export chat conversations as PDF  
- Email leads to the **respective business admin**  
- Maintain separate data, branding, and settings per business  
This makes **SmartChat a SaaS-ready product**, not a single-website chatbot.

## 🏗 Architecture Overview
### Multi-Tenant SaaS Model (One codebase → Unlimited businesses)
Each business has:
- Dedicated Business Admin 
- Unique business_key
- Isolated database records

Separate:
- Leads
- Chats
- QnA
- Settings

### 👤 Role-Based Access
#### 🔑 Super Admin
- Route: http://smartchat-br63.onrender.com/sa/login
- Credential logic:    username = "superadmin"    password = os.environ.get("SUPER_ADMIN_PASSWORD", "Admin@123")
- View & manage all businesses  
- Add & manage:
  - Business email  
  - Security key  
  - Business website  
- Monitor global leads & analytics  

#### 🧑‍💼 Business Admin
- Route: http://smartchat-br63.onrender.com/admin/login
- Credential logic:    username = "businessadmin"    password = os.environ.get("BUSINESS_ADMIN_PASSWORD", "Business_Admin@123")
- Login to own dashboard  
- Manage QnA keywords  
- View chat history & leads  
- Receive chat PDFs via email  
- Customize chat appearance  

### ✨ Core Features
#### 🧠 AI Chat Widget
- Floating AI chat button  
- Draggable chat widget & AI icon  
- Business-specific greetings  
- Keyword-based automated replies  
- Typing indicator & real-time chat  

#### 🏢 Multi-Business (SaaS Architecture)
- Unlimited businesses  
- Each business has:
  - Unique `business_key`
  - Separate chats, leads & QnA
  - Custom branding & settings  
- One codebase → many businesses  

#### 📄 Lead & PDF Automation
- Each chat session creates a **Lead**  
- Messages stored securely in database  
- Chat history exported as **Unicode-safe PDF**  
- PDF automatically emailed to the **business admin**  
- Optional webhook notifications supported  

### 🖼️ Screenshots (UrbanNest Demo)
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
```

## 🔐 Business Configuration Flow

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

## 👨‍💻 Author

Sunil Prajapati
Data Analyst | AI/ML Researcher

Project: SmartChat – Multi-Business AI Chat Platform

## ⭐ Support

If this project helps you, please ⭐ star the repository.





✨ Core Features
🤖 AI Chat Widget

Floating chat button

Draggable interface

Business-specific greeting

Keyword-based automated replies

Real-time chat flow

Session-based lead creation

📄 Lead & PDF Automation

Each chat session generates a Lead

Full conversation stored securely

Unicode-safe PDF generated using ReportLab

PDF automatically emailed to business admin

PDF stored locally under /leads/

📊 Admin Analytics (In Progress Enhancement)

Chat activity tracking

Keyword suggestions

Conversation timeline

Lead monitoring dashboard

🌐 URL Structure
Route	Purpose
/	Demo business (UrbanNest)
/sa/login	Super Admin login
/sa/dashboard	Super Admin dashboard
/admin/login	Business Admin login
/chat/<business_key>	Business chat endpoint
🛠 Tech Stack
Backend

Python

Flask

Flask-SQLAlchemy

Flask-SocketIO

Frontend

HTML

CSS (Glassmorphism UI)

JavaScript

Draggable components

Database

SQLite (Development)

PostgreSQL (Production)

Services

ReportLab (PDF generation)

SMTP Email service

Webhook-ready structure

📁 Project Structure
SmartChat/
│   app.py
│   config.py
│   models.py
│   run.py
│   create_super_admin.py
│   create_urban_admin.py
│   Procfile
│   requirements.txt
│
├── instance/
│       chat.db
│
├── leads/
│       lead_1.pdf
│       ...
│
├── services/
│       chat_engine.py
│       email_service.py
│       pdf_service.py
│
├── static/
│       chat.css
│       chat.js
│       widget_loader.js
│
├── templates/
│       admin_dashboard.html
│       admin_login.html
│       sa_dashboard.html
│       sa_login.html
│       chat_widget.html
⚙️ Local Setup
git clone https://github.com/YOUR_USERNAME/smartchat.git
cd smartchat
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
🚀 Deployment Ready

Designed for:

Render

Railway

VPS

AWS

SaaS model

Subscription-based scaling

🔮 Future Enhancements

Website auto-integration system

Subscription & billing integration

AI-based NLP enhancement

Multi-language support

Live human-agent takeover

Advanced analytics dashboard

👨‍💻 Author

Sunil Prajapati
Data Analyst | AI/ML Researcher

⭐ Support

If you find this project valuable, please star the repository.





