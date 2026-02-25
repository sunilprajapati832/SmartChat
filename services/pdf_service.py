from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
import os

# ✅ Unicode-safe font (CRITICAL)
pdfmetrics.registerFont(UnicodeCIDFont("HeiseiMin-W3"))

def generate_lead_pdf(lead, messages):
    os.makedirs("leads", exist_ok=True)
    file_path = f"leads/lead_{lead.id}.pdf"

    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    styles["Normal"].fontName = "HeiseiMin-W3"

    elements = []

    elements.append(Paragraph(f"<b>SmartChat Lead ID:</b> {lead.id}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Session:</b> {lead.session_id}", styles["Normal"]))
    elements.append(Paragraph("<br/><b>Chat Conversation</b><br/>", styles["Normal"]))

    for msg in messages:
        text = f"<b>{msg.sender.capitalize()}:</b> {msg.content}"
        elements.append(Paragraph(text, styles["Normal"]))

    doc.build(elements)
    return file_path
