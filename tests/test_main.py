import pytest
from fastapi.testclient import TestClient

from cooking_recipe_fastapi.main import app


@pytest.fixture()
def test_client() -> TestClient:
    return TestClient(app)


@pytest.mark.parametrize(
    'expected_status_code,expected_json',
    [pytest.param(200, {'msg': 'hello world!'}, id='success')])
def test_read_root(test_client, expected_status_code, expected_json) -> None:
    response = test_client.get('/')

    assert response.status_code == expected_status_code
    assert response.json() == expected_json
