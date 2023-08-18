import pytest
from fastapi.testclient import TestClient

from cooking_recipe_fastapi.main import app, ErrorMessage


@pytest.fixture()
def test_client() -> TestClient:
    return TestClient(app)


@pytest.mark.parametrize(
    'expected_status_code,expected_json',
    [pytest.param(200, {'msg': 'hello world!'}, id='success')])
def test_read_root(
        test_client: TestClient,
        expected_status_code: int,
        expected_json: dict) -> None:
    response = test_client.get('/')

    assert response.status_code == expected_status_code
    assert response.json() == expected_json


@pytest.mark.parametrize(
    'recipe_id,expected_status_code,expected_json',
    [
        pytest.param(
            111,
            400,
            {'detail': ErrorMessage.RECIPE_NOT_FOUND.value},
            id='inexistent recipe'
        ),
        pytest.param(
            3,
            200,
            {
                'id': 3,
                'label': 'Chicken Paprikash',
                'source': 'No Recipes',
                'url': 'http://norecipes.com/recipe/chicken-paprikash/'
            },
            id='success'
        )
    ])
def test_read_recipe(
        test_client: TestClient,
        recipe_id: int,
        expected_status_code: int,
        expected_json: dict) -> None:
    response = test_client.get(f'/recipes/{recipe_id}')

    assert response.status_code == expected_status_code
    assert response.json() == expected_json


@pytest.mark.parametrize(
    'label_keyword,max_results,expected_status_code,expected_json',
    [
        pytest.param(
            'chicken',
            None,
            200,
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
            id='label_keyword query parameter'),
        pytest.param(
            None,
            2,
            200,
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
            id='max_results query parameter'),
        pytest.param(
            'Chicken',
            1,
            200,
            [
                {
                    'id': 1,
                    'label': 'Chicken Vesuvio',
                    'source': 'Serious Eats',
                    'url': 'http://www.seriouseats.com/recipes/2011/12/'
                           'chicken-vesuvio-recipe.html'
                }
            ],
            id='all query parameter'),
        pytest.param(
            None,
            None,
            200,
            [
                {
                    'id': 1,
                    'label': 'Chicken Vesuvio',
                    'source': 'Serious Eats',
                    'url': 'http://www.seriouseats.com/recipes/2011/12/chicken-vesuvio'
                           '-recipe.html'
                },
                {
                    'id': 2,
                    'label': 'Cauliflower and Tofu Curry',
                    'source': 'Serious Eats',
                    'url': 'https://www.seriouseats.com/sheet-pan-cauliflower-tofu-recipe'
                },
                {
                    'id': 3,
                    'label': 'Chicken Paprikash',
                    'source': 'No Recipes',
                    'url': 'http://norecipes.com/recipe/chicken-paprikash/'
                }
            ],
            id='no query parameter'),
        pytest.param(
            'soap',
            None,
            404,
            {
                'detail': ErrorMessage.RECIPE_NOT_FOUND.value
            },
            id='nonexistent recipe')
    ])
def test_search_recipes(
        test_client: TestClient,
        label_keyword: str | None,
        max_results: int | None,
        expected_status_code: int,
        expected_json: str
) -> None:
    path = f'/recipes/search/'

    query_params = []
    if label_keyword:
        query_params.append(f'label_keyword={label_keyword}')
    if max_results:
        query_params.append(f'max_results={max_results}')

    query = f'{"?" if query_params else ""}{"&".join(query_params)}'

    if query:
        path += query

    response = test_client.get(path)

    assert response.status_code == expected_status_code
    assert response.json() == expected_json
