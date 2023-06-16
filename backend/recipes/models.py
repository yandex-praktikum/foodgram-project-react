from django.contrib.auth import get_user_model
from django.db import models

from .constants import (INGREDIENTS_NAME_MAX_LENGTH,
                        MEASUREMENT_UNIT_NAME_MAX_LENGTH)

User = get_user_model()


class Ingredients(models.Model):
    name = models.CharField(
        'Название',
        help_text='Название ингредиента',
        max_length=INGREDIENTS_NAME_MAX_LENGTH,
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        help_text='Единица измерения ингредиента',
        max_length=MEASUREMENT_UNIT_NAME_MAX_LENGTH,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_Ingredient'
            )
        ]

    def __str__(self) -> str:
        return self.name
