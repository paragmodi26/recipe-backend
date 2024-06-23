"""controller file for recipe service"""
import math
from pydantic import constr
from typing import Optional
from src.services.recipe.model import RecipeModel
from src.services.user.controller import user_details_context
from src.services.recipe.serializer import (
    RecipeSaveInbound, RecipeUpdateInbound, RecipeSingleOutbound, UserOutbound,
    IngredientsOutbound, RecipeFinalOutbound, RecipeListOutbound
)
from src.utils.common_serializers import SuccessResponsePartial, Page


class RecipeController:
    """controller class for recipe service"""
    @classmethod
    async def save(cls, payload: RecipeSaveInbound):
        """method to save recipe to database"""
        RecipeModel.create(**payload.dict())
        return SuccessResponsePartial(message="Recipe saved successfully")

    @classmethod
    async def update(cls, _id: int, payload: RecipeUpdateInbound):
        """method to update recipe to database"""
        recipe_data = RecipeModel.get_by_id(_id=_id)
        if not recipe_data:
            return SuccessResponsePartial(status="error", message="Recipe not found")
        payload_dict = payload.dict(exclude_none=True, exclude_unset=True)
        update_data = RecipeModel.patch(_id=_id, **payload_dict)
        response = None
        status = "error"
        message = "something went wrong"
        ingredients = []
        if update_data:
            created_by = UserOutbound(
                id=update_data.user.id,
                name=update_data.user.name,
            )
            for each in update_data.ingredients:
                ingredients.append(IngredientsOutbound(
                    name=each.get("name"),
                    quantity=each.get("quantity")
                ))
            response = RecipeSingleOutbound(
                id=update_data.id,
                name=update_data.name,
                title=update_data.title,
                description=update_data.description,
                ingredients=ingredients,
                instructions=update_data.instructions,
                created_by=created_by
            )
            message = "Recipe updated successfully"
            status = "success"
        return RecipeFinalOutbound(data=response, message=message, status=status)

    @classmethod
    async def delete(cls, _id: int):
        """method to delete recipe from database"""
        user_details = user_details_context.get()
        exists_data = RecipeModel.get_by_id(_id=_id, user_id=user_details.id)
        if not exists_data:
            return SuccessResponsePartial(status="error", message="Recipe not found")
        RecipeModel.delete(_id=_id)
        return SuccessResponsePartial(message="Recipe deleted successfully")

    @classmethod
    async def get_list(
        cls,
        page: int = 1, limit: int = 10,
        search_keyword: Optional[constr(min_length=2, max_length=200)] = None,
        is_all: bool = True,
    ):
        """method to get recipe list from database"""
        user_details = user_details_context.get()
        recipe_data, total_count = RecipeModel.get_all(
            page=page, limit=limit, search_keyword=search_keyword, is_all=is_all,
            user_id=user_details.id
        )
        page = Page(
            page_size=len(recipe_data),
            total_results=total_count,
            page_number=page,
            num_pages=math.ceil(total_count / limit),
        )
        response = []
        for data in recipe_data or []:
            created_by = UserOutbound(
                id=data.user.id,
                name=data.user.name,
            )
            ingredients = []
            for each in data.ingredients:
                ingredients.append(IngredientsOutbound(
                    name=each.get("name"),
                    quantity=each.get("quantity")
                ))
            response.append(RecipeSingleOutbound(
                id=data.id,
                name=data.name,
                title=data.title,
                description=data.description,
                ingredients=ingredients,
                instructions=data.instructions,
                created_by=created_by
            ))
        return RecipeListOutbound(data=response, page=page)

    @classmethod
    async def get_by_id(cls, _id: int):
        """method to get data by id"""
        recipe_data = RecipeModel.get_by_id(_id=_id)
        if not recipe_data:
            return SuccessResponsePartial(status="error", message="Recipe not found")
        created_by = UserOutbound(
            id=recipe_data.user.id,
            name=recipe_data.user.name,
        )
        ingredients = []
        for each in recipe_data.ingredients:
            ingredients.append(IngredientsOutbound(
                name=each.get("name"),
                quantity=each.get("quantity")
            ))
        response = RecipeSingleOutbound(
            id=recipe_data.id,
            name=recipe_data.name,
            title=recipe_data.title,
            description=recipe_data.description,
            ingredients=ingredients,
            instructions=recipe_data.instructions,
            created_by=created_by
        )
        return RecipeFinalOutbound(data=response)