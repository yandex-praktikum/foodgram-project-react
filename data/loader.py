import json

with open('ingredients.json', 'r') as file:
    db_data = []
    db_data.append(
        {"model": "recipes.tag", "pk": 1,
         "fields": {"name": "завтрак",
                    "color": "#008000",
                    "slug": "breakfast"}})
    db_data.append({"model": "recipes.tag", "pk": 2,
                    "fields": {"name": "обед",
                               "color": "#9E6607",
                               "slug": "lunch"}})
    db_data.append({"model": "recipes.tag", "pk": 3,
                    "fields": {"name": "ужин",
                               "color": "#1E67BD",
                               "slug": "dinner"}})
    data = json.load(file)
    for i, ingredient in enumerate(data):
        db_data.append({"model": "recipes.ingredient", "pk": i + 1,
                        "fields": {"name": ingredient.get("name"),
                                   "measurement_unit":
                                   ingredient.get("measurement_unit")}})
    print(f'db writed to dumping file. Total {len(db_data)} items')

with open('dump.json', 'w', encoding='utf-8') as file:
    json.dump(db_data, file, ensure_ascii=False, indent=2)
