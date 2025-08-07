# services/pdf_generator.py

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import os

def generate_booking_receipt(user_name, date_str, time_str, file_path):
    doc = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = [Paragraph("رسید رزرو وقت", styles['Title']), Spacer(1, 12),
             Paragraph(f"نام: {user_name}", styles['Normal']), Paragraph(f"تاریخ رزرو: {date_str}", styles['Normal']),
             Paragraph(f"ساعت رزرو: {time_str}", styles['Normal']), Spacer(1, 12),
             Paragraph("✅ لطفاً این رسید را نگه‌داری کنید.", styles['Italic'])]

    doc.build(story)
