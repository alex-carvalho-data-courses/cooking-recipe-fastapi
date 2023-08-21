from enum import StrEnum, unique
from fastapi import APIRouter, FastAPI, HTTPException
from http import HTTPStatus

from cooking_recipe_fastapi.recipes_data import RecipesFakeDB, RECIPE_SEED_DATA
from cooking_recipe_fastapi.schemas import (
    Recipe, RecipeCreate, RecipeSearchResults)

fake_db = RecipesFakeDB(RECIPE_SEED_DATA)


@unique
class ErrorMessage(StrEnum):
    RECIPE_NOT_FOUND = 'Recipe not found'


app = FastAPI(title='Cooking recipe API', openapi_url='/openapi.json')
api_router = APIRouter()


@api_router.get('/', status_code=HTTPStatus.OK)
async def read_root() -> dict:
    return {'msg': 'hello world!'}


@api_router.get(
    '/recipes/{recipe_id}', status_code=HTTPStatus.OK, response_model=Recipe)
async def read_recipe(recipe_id: int) -> dict:
    recipe = fake_db.recipe.get(recipe_id)

    if recipe:
        return recipe

    raise HTTPException(
        HTTPStatus.NOT_FOUND, ErrorMessage.RECIPE_NOT_FOUND)


@api_router.get(
    path='/recipes/search/',
    status_code=HTTPStatus.OK,
    response_model=RecipeSearchResults)
async def search_recipes(
        label_keyword: str | None = None,
        max_results: int | None = 10) -> dict:
    recipes = fake_db.recipe.search(label_keyword, max_results)

    if recipes:
        return {'results': recipes[:max_results]}
    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=ErrorMessage.RECIPE_NOT_FOUND)


@api_router.post(
    path='/recipes/', status_code=HTTPStatus.CREATED)
async def create_recipe(recipe: RecipeCreate) -> dict:
    recipe = recipe.model_dump()
    recipe.pop('submitter_id')

    recipe = fake_db.recipe.add(recipe)
    print(recipe)

    return {'resource_path': f'/recipes/{recipe["id"]}'}


app.include_router(api_router)


if __name__ == '__main__':
    # Approach only for debug
    import uvicorn

    uvicorn.run(
        app, host='0.0.0.0', port=8001, log_level='debug')
    