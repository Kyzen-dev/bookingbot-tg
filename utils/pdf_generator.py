from reportlab.lib.pagesizes import A6
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
from reportlab.pdfgen import canvas
import os
import arabic_reshaper
from bidi.algorithm import get_display

pdfmetrics.registerFont(TTFont('Vazir', 'asset/font/Vazirmatn-Regular.ttf'))
def reshape_text(text):
    reshaped_text = arabic_reshaper.reshape(text)  # اتصال حروف
    bidi_text = get_display(reshaped_text)         # اصلاح جهت متن
    return bidi_text


def draw_background(canvas, doc):
    canvas.setFillColor(HexColor("#f0f0f0"))
    canvas.rect(0, 0, A6[0], A6[1], fill=True, stroke=0)

def generate_booking_pdf(data, file_path="receipt.pdf", tracking_code=None):
    doc = SimpleDocTemplate(file_path, pagesize=A6,
                            rightMargin=10, leftMargin=10,
                            topMargin=20, bottomMargin=10)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT, fontName='Vazir', fontSize=11))

    story = []

    logo_path = "asset/logo_bot.png"
    if os.path.exists(logo_path):
        story.append(Image(logo_path, width=40 * mm, height=15 * mm))
        story.append(Spacer(1, 6))

    texts = [
        f"نام: {data.get('name', '-')}",
        f"شماره تماس: {data.get('phone', '-')}",
        f"تاریخ رزرو: {data.get('date', '-')}",
        f"ساعت: {data.get('time', '-')}",
        f"سرویس: {data.get('service', '-')}",
        f"یادداشت: {data.get('notes', '-')}",
        f"کد پیگیری:{data.get('ref_code', tracking_code or '-')}",
    ]

    for txt in texts:
        reshaped_txt = reshape_text(txt)
        story.append(Paragraph(reshaped_txt, styles['Right']))
        story.append(Spacer(1, 4))

    doc.build(story, onFirstPage=draw_background, onLaterPages=draw_background)
    return file_path