import io

from django.http.response import FileResponse
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from core.services import prepare_ingredients_list


def create_pdf_report(items):
    """Создаем отчёт в виде PDF-файла."""
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    pdfmetrics.registerFont(TTFont('IntelOneMono-Regular', 'fonts/IntelOneMono-Regular.ttf'))
    p.setFont('IntelOneMono-Regular', 14)
    p.drawCentredString(
        300, 800,
        'Список покупок:')
    text_object = p.beginText(2 * cm, 29.7 * cm - 2 * cm)
    for line in prepare_ingredients_list(items).splitlines(False):
        text_object.textLine(line.rstrip())
    p.drawText(text_object)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True,
                        filename='shopping_list.pdf')
