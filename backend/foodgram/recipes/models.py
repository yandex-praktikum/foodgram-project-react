from django.db.models import CharField, Model, SlugField


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


class Tag(Model):
    name = CharField(
        verbose_name='Название тега',
        help_text='Введите название тега',
        max_length=200,
        unique=True
    )
    color = CharField(
        verbose_name='Цвет в НЕХ',
        help_text='Выбирите цвет',
        max_length=7,
        unique=True,
        blank=True,
        null=True
    )
    slug = SlugField(
        verbose_name='Слаг тега',
        help_text='Введите слаг тега',
        max_length=200,
        unique=True
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return {self.name}
