import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from django.conf import settings
import os

def generate_invoice_pdf(participant):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=40, leftMargin=40,
                            topMargin=60, bottomMargin=40)

    styles = getSampleStyleSheet()
    story = []

    # 🔹 Logo & Header
    logo_path = os.path.join(settings.BASE_DIR, "static", "img", "logoaiml.png")
    if os.path.exists(logo_path):
        img = Image(logo_path, width=100, height=50)
        story.append(img)
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>AIML Paris Conference 2025</b>", styles['Title']))
    story.append(Paragraph("Registration Invoice / Receipt", styles['Heading2']))
    story.append(Spacer(1, 24))

    # 🔹 Invoice Info Table
    invoice_data = [
        ["Invoice ID", f"#{participant.id}"],
        ["Name", participant.name],
        ["Email", participant.email],
        ["Organization", participant.organization or "-"],
        ["Registration Type", participant.get_registration_type_display()],
        ["Amount Paid", f"${participant.amount_paid} USD"],
        ["Status", "PAID ✅"],
        ["Date", participant.created_at.strftime('%B %d, %Y %H:%M')],
    ]

    table = Table(invoice_data, colWidths=[150, 350])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f2f2f2")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
    ]))
    story.append(table)
    story.append(Spacer(1, 24))

    # 🔹 Footer
    footer_text = "This is an auto-generated invoice. For any questions, contact info@aiml-paris.com"
    story.append(Paragraph(footer_text, styles['Normal']))

    doc.build(story)
    buffer.seek(0)
    return buffer



from datetime import date

def get_fee(category, reg_type):
    today = date.today()
    early_deadline = date(2025, 10, 1)
    late = today > early_deadline
    fees = {
        'member': {'student': (50, 70), 'regular': (100, 130), 'industrial': (200, 250)},
        'non-member': {'student': (70, 90), 'regular': (130, 160), 'industrial': (250, 300)},
    }
    early_fee, late_fee = fees[category][reg_type]
    return late_fee if late else early_fee



from datetime import date

# Set your early registration deadline
EARLY_BIRD_DEADLINE = date(2025, 10, 1)

def is_late_registration():
    return date.today() >= EARLY_BIRD_DEADLINE

def get_fee(category, reg_type):
    """
    Return fee in USD based on category, type and date.
    """
    late = is_late_registration()

    # Fee structure: (early_fee, late_fee)
    fees = {
        'member': {
            'student': (50, 70),
            'regular': (100, 130),
            'industrial': (200, 250)
        },
        'non-member': {
            'student': (70, 90),
            'regular': (130, 160),
            'industrial': (250, 300)
        }
    }

    early_fee, late_fee = fees[category][reg_type]
    return late_fee if late else early_fee
