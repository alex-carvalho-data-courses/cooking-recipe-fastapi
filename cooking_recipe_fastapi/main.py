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
        'label': 'Chicken Paprikash',
        'source': 'No Recipes',
        'url': 'http://norecipes.com/recipe/chicken-paprikash/'
    },
    {
        'id': 3,
        'label': 'Cauliflower and Tofu Curry',
        'source': 'Serious Eats',
        'url': 'https://www.seriouseats.com/sheet-pan-cauliflower-tofu-recipe'
    }
]

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

    raise HTTPException(400, 'Recipe not found')


app.include_router(api_router)


if __name__ == '__main__':
    # Approach only for debug
    import uvicorn

    uvicorn.run(
        app, host='0.0.0.0', port=8001, log_level='debug')
    