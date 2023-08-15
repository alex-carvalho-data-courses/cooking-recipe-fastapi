from fastapi import APIRouter, FastAPI

app = FastAPI(title='Cooking recipe API', openapi_url='/openapi.json')
api_router = APIRouter()


@api_router.get('/', status_code=200)
async def read_root() -> dict:
    return {'msg': 'hello world!'}

app.include_router(api_router)


if __name__ == '__main__':
    # Approach only for debug
    import uvicorn

    uvicorn.run(
        app, host='0.0.0.0', port=8001, log_level='debug')
    