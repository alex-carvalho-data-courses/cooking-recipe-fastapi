from enum import Enum, unique
from fastapi import APIRouter, FastAPI, HTTPException

RECIPES = [
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


@unique
class ErrorMessage(Enum):
    RECIPE_NOT_FOUND = 'Recipe not found'


app = FastAPI(title='Cooking recipe API', openapi_url='/openapi.json')
api_router = APIRouter()


@api_router.get('/', status_code=200)
async def read_root() -> dict:
    return {'msg': 'hello world!'}


@api_router.get('/recipes/{recipe_id}', status_code=200)
async def read_recipe(recipe_id: int) -> dict:
    for recipe in RECIPES:
        if recipe['id'] == recipe_id:
            return recipe

    raise HTTPException(400, ErrorMessage.RECIPE_NOT_FOUND.value)


@api_router.get('/recipes/search/', status_code=200)
async def search_recipes(
        label_keyword: str | None = None,
        max_results: int | None = 10) -> list[dict]:
    recipes = RECIPES

    if label_keyword:
        recipes = [recipe for recipe in RECIPES
                   if label_keyword.lower() in str(recipe['label']).lower()]

    if recipes[:max_results]:
        return recipes[:max_results]
    else:
        raise HTTPException(
            status_code=404, detail=ErrorMessage.RECIPE_NOT_FOUND.value)


app.include_router(api_router)


if __name__ == '__main__':
    # Approach only for debug
    import uvicorn

    uvicorn.run(
        app, host='0.0.0.0', port=8001, log_level='debug')
    