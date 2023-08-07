from recipes.models import Recipe


def get_all_recipes() -> Recipe:
    """Возвращает список всех рецептов."""

    return Recipe.objects.all()  # WIP: Доступна фильтрация по избранному, автору, списку покупок и тегам.
