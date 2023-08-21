RECIPE_SEED_DATA = {
    1: {
        'id': 1,
        'label': 'Chicken Vesuvio',
        'source': 'Serious Eats',
        'url': 'http://www.seriouseats.com/recipes/2011/12/chicken-vesuvio'
               '-recipe.html'
    },
    2: {
        'id': 2,
        'label': 'Cauliflower and Tofu Curry',
        'source': 'Serious Eats',
        'url': 'https://www.seriouseats.com/sheet-pan-cauliflower-tofu-recipe'
    },
    3: {
        'id': 3,
        'label': 'Chicken Paprikash',
        'source': 'No Recipes',
        'url': 'http://norecipes.com/recipe/chicken-paprikash/'
    }
}


class Table:
    def __init__(self, name: str, seed_data: dict[int, dict] | None) -> None:
        self.name = name
        self._data: dict[int, dict] = seed_data.copy() if seed_data else {}

    def get(self, data_id: int) -> dict:
        return self._data.get(data_id)

    @staticmethod
    def get_next_id(fake_table_data: dict[int, dict]) -> int:
        return max(fake_table_data.keys()) + 1

    def add(self, data: dict) -> dict:
        data_id = self.get_next_id(self._data)

        new_row = {'id': data_id}
        data.pop('id', None)
        new_row.update(data)

        self._data.update({data_id: new_row})

        return new_row

    def delete(self, data_id: int) -> int | None:
        try:
            self._data.pop(data_id)

            return data_id
        except KeyError:
            return None

    def update(self, data_id: int, fields: dict) -> dict:
        item = self.get(data_id)

        if item:
            item.update(fields)

        return item


class RecipeTable(Table):
    def __init__(self, seed_data: dict[int, dict] | None) -> None:
        super().__init__('recipe', seed_data)

    def search(
            self,
            label_keyboard: str | None = None,
            max_results: int = 10) -> list[dict]:
        if label_keyboard:
            recipes = [
                recipe for recipe in self._data.values()
                if label_keyboard.lower() in str(recipe['label']).lower()
            ]

            if recipes:
                recipes = recipes[:max_results]
        else:
            recipes = list(self._data.values())[:max_results]

        return recipes


class RecipesFakeDB:
    def __init__(self, recipe_seed_data: dict[int, dict] | None) -> None:
        self.recipe = RecipeTable(recipe_seed_data)


