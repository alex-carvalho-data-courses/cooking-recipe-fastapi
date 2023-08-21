import pytest

from cooking_recipe_fastapi.recipes_data import RecipesFakeDB, RECIPE_SEED_DATA, Table

RECIPE_BOLIVIAN_FEIJOADA = {
    'label': 'Feijoada Boliviana',
    'source': 'Curious Cuisiniere',
    'url': 'https://www.curiouscuisiniere.com/'
           'feijoada-brazilian-black-bean-stew/'
}


@pytest.fixture
def fake_db() -> RecipesFakeDB:
    return RecipesFakeDB(RECIPE_SEED_DATA)


@pytest.mark.parametrize(
    'fake_table,expected_id',
    [
        pytest.param(
            {
                11: {
                    'id': 11,
                    'name': 'bett'
                },
                13: {
                    'id': 13,
                    'name': 'stul'
                }
            },
            14,
            id='success'
        )
    ])
def test_get_next_id(
        fake_db: RecipesFakeDB,
        fake_table: dict[int, dict],
        expected_id: int) -> None:
    assert Table.get_next_id(fake_table) == expected_id


@pytest.mark.parametrize(
    'recipe_id,expected_row',
    [
        pytest.param(
            2,
            {
                'id': 2,
                'label': 'Cauliflower and Tofu Curry',
                'source': 'Serious Eats',
                'url': 'https://www.seriouseats.com/'
                       'sheet-pan-cauliflower-tofu-recipe'
            },
            id='tofu curry - from seed data'),
        pytest.param(
            20,
            None,
            id='No recipe for Id.'
        )
    ])
def test_recipe_get(
        fake_db: RecipesFakeDB, recipe_id: int, expected_row: dict) -> None:
    assert fake_db.recipe.get(recipe_id) == expected_row


@pytest.mark.parametrize(
    'label_keyword,max_results,expected_result_list',
    [
        pytest.param(
            None,
            None,
            list(RECIPE_SEED_DATA.values()),
            id='no params'),
        pytest.param(
            'chicken',
            None,
            [
                {
                    'id': 1,
                    'label': 'Chicken Vesuvio',
                    'source': 'Serious Eats',
                    'url': 'http://www.seriouseats.com/recipes/2011/12/chicken-vesuvio'
                           '-recipe.html'
                },
                {
                    'id': 3,
                    'label': 'Chicken Paprikash',
                    'source': 'No Recipes',
                    'url': 'http://norecipes.com/recipe/chicken-paprikash/'
                }
            ],
            id='chicken keyword-return 2'),
        pytest.param(
            'tofu',
            None,
            [
                {
                    'id': 2,
                    'label': 'Cauliflower and Tofu Curry',
                    'source': 'Serious Eats',
                    'url': 'https://www.seriouseats.com/sheet-pan-cauliflower-tofu-recipe'
                }
            ],
            id='tofu keyword-return 1'),
        pytest.param(
            'angu',
            None,
            [],
            id='angu keyword-return nothing'),
        pytest.param(
            None,
            2,
            [
                {
                    'id': 1,
                    'label': 'Chicken Vesuvio',
                    'source': 'Serious Eats',
                    'url': 'http://www.seriouseats.com/recipes/2011/12/'
                           'chicken-vesuvio-recipe.html'
                },
                {
                    'id': 2,
                    'label': 'Cauliflower and Tofu Curry',
                    'source': 'Serious Eats',
                    'url': 'https://www.seriouseats.com/'
                           'sheet-pan-cauliflower-tofu-recipe'
                }
            ],
            id='max_results 2')
    ])
def test_recipe_search(
        fake_db: RecipesFakeDB,
        label_keyword: str | None,
        max_results: int | None,
        expected_result_list: list[dict] | None) -> None:
    if max_results:
        recipes = fake_db.recipe.search(label_keyword, max_results)
    else:
        recipes = fake_db.recipe.search(label_keyword)

    assert recipes == expected_result_list


@pytest.mark.parametrize(
    'recipe,expected_recipe_with_id',
    [
        pytest.param(
            RECIPE_BOLIVIAN_FEIJOADA,
            {
                'id': 4,
                **RECIPE_BOLIVIAN_FEIJOADA
            },
            id='create feijoada')
    ]
)
def test_recipe_add(
        fake_db: RecipesFakeDB,
        recipe: dict,
        expected_recipe_with_id: dict) -> None:
    assert fake_db.recipe.add(recipe) == expected_recipe_with_id


@pytest.mark.parametrize(
    'recipe,expected_recipe_with_id',
    [
        pytest.param(
            RECIPE_BOLIVIAN_FEIJOADA,
            {
                'id': 5,
                **RECIPE_BOLIVIAN_FEIJOADA
            },
            id='create feijoada - insert twice same item - different id')
    ]
)
def test_recipe_add_existent(
        fake_db: RecipesFakeDB,
        recipe: dict,
        expected_recipe_with_id: dict) -> None:
    fake_db.recipe.add(recipe)

    assert fake_db.recipe.add(recipe) == expected_recipe_with_id


@pytest.mark.parametrize(
    'recipe_id,expected_response_id',
    [
        pytest.param(2, 2, id='delete existent item'),
        pytest.param(20, None, id='delete nonexistent item')
    ])
def test_recipe_delete(
        fake_db: RecipesFakeDB,
        recipe_id: int,
        expected_response_id: int | None) -> None:
    assert fake_db.recipe.delete(recipe_id) == expected_response_id


@pytest.mark.parametrize(
    'recipe_id,update_data,expected_dict',
    [
        pytest.param(
            2,
            {'label': 'Chicken and Tofu Curry'},
            {
                'id': 2,
                'label': 'Chicken and Tofu Curry',
                'source': 'Serious Eats',
                'url': 'https://www.seriouseats.com/sheet-pan-cauliflower-tofu-recipe'
            },
            id='update partial'),
        pytest.param(
            3,
            {
                'id': 3,
                'label': 'Chicken Paprikash',
                'source': 'No Recipes',
                'url': 'http://norecipes.com/recipe/chicken-paprikash/'
            },
            {
                'id': 3,
                'label': 'Chicken Paprikash',
                'source': 'No Recipes',
                'url': 'http://norecipes.com/recipe/chicken-paprikash/'
            },
            id='update full'),
        pytest.param(
            5,
            {'label': 'Chicken and Tofu Curry'},
            None,
            id='non existent item')
    ])
def test_recipe_update(
        fake_db: RecipesFakeDB,
        recipe_id: int,
        update_data: dict,
        expected_dict: dict) -> None:
    assert fake_db.recipe.update(recipe_id, update_data) == expected_dict
