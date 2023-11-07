from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
def validation_400(value):
    """Свой кастыльный валидатор"""
    if not value:
        #error_message = "Ингридиента не существует!"
        return Response(status=status.HTTP_400_BAD_REQUEST)
