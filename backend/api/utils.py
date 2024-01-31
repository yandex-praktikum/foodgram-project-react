import io

from django.db.models.aggregates import Sum
from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

FILENAME = 'shoppingcart.pdf'


def create_shopping_cart(ingredients_cart):
    """Создаем список с ингредиентами."""

    response = HttpResponse(content_type='applications/pdf')
    response['Content-Disposition'] = (
        "attachment; filename='shopping_Cart.pdf'"
    )
    buffer = io.BytesIO()
    page = canvas.Canvas(buffer)
    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    x_position, y_position = 50, 800
    shopping_cart = (
        ingredients_cart.values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('recipe__amount')).order_by())
    page.setFont('Vera', 14)
    if shopping_cart:
        indent = 20
        page.drawString(x_position, y_position, 'Cписок покупок:')
        for index, recipe in enumerate(shopping_cart, start=1):
            page.drawString(
                x_position, y_position - indent,
                f'{index}. {recipe["ingredient__name"]} - '
                f'{recipe["recipe__amount"]} '
                f'{recipe["ingredient__measurement_unit"]}.')
            y_position -= 15
            if y_position <= 50:
                page.showPage()
                y_position = 800
        page.save()
        pdf = buffer.getvalue()
        buffer.close
        response.write(pdf)
        return response
    page.setFont('Vera', 24)
    page.drawString(
        x_position,
        y_position,
        'Cписок покупок пуст!')
    page.save()
    pdf = buffer.getvalue()
    buffer.close
    response.write(pdf)
    return response
