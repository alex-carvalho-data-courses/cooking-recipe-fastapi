from pydantic import BaseModel, HttpUrl
from typing import Sequence


class Recipe(BaseModel):
    id: int | None = None
    label: str
    source: str
    url: HttpUrl


class RecipeSearchResults(BaseModel):
    results: Sequence[Recipe]


class RecipeCreate(Recipe):
    submitter_id: int
