# <img src="img/cooking-recipe.png" alt="cooking recipe project" width="30" style="vertical-align: middle;"> <img src="img/fastapi-logo-green.png" alt="FastAPI" width="30" style="vertical-align: middle;"> | Cooking Recipe API - with FastAPI

## What is this repository for? ##

### Quick summary

tutorial project to create a cooking recipe API - FastAPI.  
based on [The FastAPI Ultimate Tutorial](https://christophergs.com/python/2021/12/04/fastapi-ultimate-tutorial/) - by [Christopher Samiullah](https://christophergs.com/)


## How do I get set up? ##

### Summary of set up

In a environment with Python and Poetry already installed, issue the command:  
```shell
poetry install
```

### Dependencies

- python ^3.11
- poetry ^1.4.2
- FastAPI ^0.101.0 (main python dependency managed by poetry)  

### Configuration

CHANGE_ME  

### Database configuration

CHANGE_ME  

### How to run tests

#### Automated  
```shell
poetry run pytest
```

#### Manual

##### 1. start uvicorn server
```shell
uvicorn cooking_recipe_fastapi.main:app --reload
```

##### 2. Trigger manual tests from documentation

http://127.0.0.1:8000/docs

### Deployment instructions

CHANGE_ME  


## Who do I talk to? ##

### Repo owner or admin

[alex carvalho](mailto:allex.carvalho@gmail.com)
