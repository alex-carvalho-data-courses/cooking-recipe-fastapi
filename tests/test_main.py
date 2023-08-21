import pytest
from fastapi.testclient import TestClient
from http import HTTPStatus

from cooking_recipe_fastapi.main import app, ErrorMessage


@pytest.fixture()
def test_client() -> TestClient:
    return TestClient(app)


@pytest.mark.parametrize(
    'expected_status_code,expected_json',
    [pytest.param(HTTPStatus.OK, {'msg': 'hello world!'}, id='success')])
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
            HTTPStatus.NOT_FOUND,
            {'detail': ErrorMessage.RECIPE_NOT_FOUND.value},
            id='nonexistent recipe'
        ),
        pytest.param(
            3,
            HTTPStatus.OK,
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
            HTTPStatus.OK,
            {
                'results': [
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
                ]
            },
            id='label_keyword query parameter'),
        pytest.param(
            None,
            2,
            HTTPStatus.OK,
            {
                'results': [
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
                ]
            },
            id='max_results query parameter'),
        pytest.param(
            'Chicken',
            1,
            HTTPStatus.OK,
            {
                'results': [
                    {
                        'id': 1,
                        'label': 'Chicken Vesuvio',
                        'source': 'Serious Eats',
                        'url': 'http://www.seriouseats.com/recipes/2011/12/'
                               'chicken-vesuvio-recipe.html'
                    }
                ]
            },
            id='all query parameter'),
        pytest.param(
            None,
            None,
            HTTPStatus.OK,
            {
                'results': [
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
                ]
            },
            id='no query parameter'),
        pytest.param(
            'soap',
            None,
            HTTPStatus.NOT_FOUND,
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
        expected_json: str) -> None:
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


@pytest.mark.parametrize(
    'new_recipe,expected_status_code,expected_response',
    [
        pytest.param(
            {
                'label': 'Feijoada Boliviana',
                'source': 'Curious Cuisiniere',
                'url': 'https://www.curiouscuisiniere.com/'
                       'feijoada-brazilian-black-bean-stew/',
                'submitter_id': 123
            },
            HTTPStatus.CREATED,
            {'resource_path': '/recipes/4'},
            id='success'),
        pytest.param(
            {
                'source': 'Curious Cuisiniere',
                'submitter_id': 123
            },
            HTTPStatus.UNPROCESSABLE_ENTITY,
            None,
            id='missing properties request body'),
        pytest.param(
            {
                'label': 'Feijoada Boliviana',
                'source': 'Curious Cuisiniere',
                'url': 'https://www.curiouscuisiniere.com/'
                       'feijoada-brazilian-black-bean-stew/',
                'submitter_id': 123,
                'something': 'else'
            },
            HTTPStatus.CREATED,
            {'resource_path': '/recipes/5'},
            id='additional parameter')
    ])
def test_recipe_create(
        test_client: TestClient,
        new_recipe: dict,
        expected_status_code: int,
        expected_response: int) -> None:
    response = test_client.post(
        '/recipes/',
        json=new_recipe)

    assert response.status_code == expected_status_code

    if expected_status_code == HTTPStatus.CREATED:
        assert response.json() == expected_response
    else:
        assert 'detail' in response.json()
