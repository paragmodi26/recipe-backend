"""serilzier file for recipe services"""
from pydantic import BaseModel, constr
from typing import Optional, List
from src.utils.common_serializers import SuccessResponsePartial


class IngredientsInbound(BaseModel):
    """ingredients serializer class for recipe"""
    name: str
    quantity: str


class IngredientsOutbound(BaseModel):
    """ingredients serializer class for recipe"""
    name: Optional[str] = None
    quantity: Optional[str] = None


class UserOutbound(BaseModel):
    """user outbound serializer class for recipe"""
    id: Optional[int] = None
    name: Optional[str] = None


class RecipeSaveInbound(BaseModel):
    """recipe inbound serializer class for save recipe"""
    name: constr(max_length=250)
    title: constr(max_length=255)
    description: Optional[str] = None
    ingredients: Optional[List[IngredientsInbound]] = None
    instructions: Optional[str] = None


class RecipeUpdateInbound(BaseModel):
    """recipe inbound serializer class for update recipe"""
    name: Optional[constr(max_length=250)] = None
    title: Optional[constr(max_length=255)] = None
    description: Optional[str] = None
    ingredients: Optional[List[IngredientsInbound]] = None
    instructions: Optional[str] = None


class RecipeSingleOutbound(BaseModel):
    """recipe single data outbound"""
    id: Optional[int] = None
    name: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    ingredients: Optional[List[IngredientsOutbound]] = None
    instructions: Optional[str] = None
    created_by: Optional[UserOutbound] = None


class RecipeFinalOutbound(SuccessResponsePartial):
    """recipe final outbound"""
    data: Optional[RecipeSingleOutbound] = None


class RecipeListOutbound(SuccessResponsePartial):
    """recipe final outbound"""
    data: Optional[List[RecipeSingleOutbound]] = None
