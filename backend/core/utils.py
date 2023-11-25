from recipes.models import IngredientRecipe, User
from django.db.models import Sum
from django.http import HttpResponse

FILENAME = "shopping_cart.txt"
HEADER_FILE_CART = (
    "Не порть продукты, сходи в ресторан:\n\nИнгредиент   -   Кол-во/Ед.изм.\n"
)

    
def ingredient_recipe(recipe, ingredients):
    selected_ingredients = []
    for ingredient, amount in ingredients.values():
        selected_ingredients.append(
            IngredientRecipe(
                recipe=recipe, ingredients=ingredient, amount=amount
            )
        )

def create_shoping_list(user: 'User'):
        ingredients = (
            IngredientRecipe.objects.filter(recipe__cart__user=user)
            .values("ingredient__name", "ingredient__measurement_unit")
            .order_by("ingredient__name")
            .annotate(total=Sum("amount"))
        )
        result = HEADER_FILE_CART
        result += "\n".join(
            [
                f'{ingredient["ingredient__name"]} - {ingredient["total"]}/'
                f'{ingredient["ingredient__measurement_unit"]}'
                for ingredient in ingredients
            ]
        )
        response = HttpResponse(result, content_type="text/plain")
        response["Content-Disposition"] = f"attachment; filename={FILENAME}"
        print(response)
        return response
