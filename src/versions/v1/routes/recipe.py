"""route file for recipe route."""
from typing import Optional
from fastapi import APIRouter, Request
from pydantic import conint, constr
from src.services.recipe.controller import RecipeController
from src.services.recipe.serializer import RecipeSaveInbound, RecipeUpdateInbound
from src.utils.auth import Auth


router = APIRouter()


@router.post('/save')
@Auth.authenticate_user
async def save(request: Request, payload: RecipeSaveInbound):
    """route to save new recipe"""
    return await RecipeController.save(payload=payload)


@router.patch('/{id}')
@Auth.authenticate_user
async def update(request: Request, id: conint(gt=0), payload: RecipeUpdateInbound):
    """route to save new recipe"""
    return await RecipeController.update(_id=id, payload=payload)


@router.delete('/{id}')
@Auth.authenticate_user
async def delete(request: Request, id: conint(gt=0)):
    """route to save new recipe"""
    return await RecipeController.delete(_id=id)

@router.get('/all')
@Auth.authenticate_user
async def get_recipes(
    request: Request,
    page: int = 1, limit: int = 10,
    search_keyword: Optional[constr(min_length=2, max_length=200)] = None,
    is_all: bool = True,
):
    """router to get all recipes"""
    return await RecipeController.get_list(
        page=page, limit=limit,
        search_keyword=search_keyword, is_all=is_all
    )


@router.get('/{id}')
@Auth.authenticate_user
async def get_by_id(request: Request, id: conint(gt=0)):
    """route to get recipe by id"""
    return await RecipeController.get_by_id(_id=id)

