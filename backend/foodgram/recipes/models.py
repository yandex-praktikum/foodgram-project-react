from django.db.models import CharField, Model


class Ingredient(Model):
    name = CharField(
        verbose_name='Название ингредиента',
        help_text='Введите ингредиент',
        max_length=200
    )
    measurement_unit = CharField(
        verbose_name='Единица измерения',
        help_text='Введите единицу измерения',
        max_length=200
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return {self.name}
