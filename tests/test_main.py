import pytest
from fastapi.testclient import TestClient

from cooking_recipe_fastapi.main import app


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
            {'detail': 'Recipe not found'},
            id='inexistent recipe'
        ),
        pytest.param(
            2,
            200,
            {
                'id': 2,
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
