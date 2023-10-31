from django.core.validators import RegexValidator, MinValueValidator


class HexCheckValidation(RegexValidator):
    '''Валидатор корректности ввода цвета'''
    message = 'введите цвет в формате HEX!'
    regex = '^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'


class MinValueTimeCookingValidator(MinValueValidator):
    '''Валидатор корректности вводимого значения времени
     приготовления в рецепте'''
    limit_value = 1
    message = 'не менее 1 минуты!'
