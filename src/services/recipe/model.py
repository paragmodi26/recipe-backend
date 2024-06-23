"""model file for recipe service."""
from sqlalchemy import or_, cast, String
from src.db.session import save_new_row, get_db, update_old_row, select_first, delete, select_all, select_count
from src.schema.schema import RecipeSchema
from src.services.user.controller import user_details_context

db = get_db()


class RecipeModel:
    """recipe Model"""
    @classmethod
    def create(cls, **kw):
        """method to save new recipe in database"""
        obj = RecipeSchema(**kw)
        obj.created_by = user_details_context.get().id
        save_new_row(obj)
        return obj

    @classmethod
    def patch(cls, _id: int, **kw):
        """method to update data"""
        row = db.query(RecipeSchema).filter(RecipeSchema.id == _id).first()
        for key, value in kw.items():
            setattr(row, key, value)
        update_old_row(row)
        return cls.get_by_id(_id=_id)

    @classmethod
    def get_by_id(cls, _id: int, user_id: int = None):
        """method to get data by id"""
        query = db.query(RecipeSchema).filter(RecipeSchema.id == _id)
        if user_id:
            query = query.filter(RecipeSchema.created_by == user_id)
        query = select_first(query)
        return query

    @classmethod
    def delete(cls, _id: int):
        """delete by id"""
        query = db.query(RecipeSchema).filter(RecipeSchema.id == _id)
        query = delete(query)
        return query

    @classmethod
    def get_all(
        cls, page: int = 1, limit: int = 10,
        search_keyword: str = None, is_all: bool = True, user_id: int = None
    ):
        """method to get all data"""
        query = db.query(RecipeSchema)
        if search_keyword:
            query = query.filter(or_(
                RecipeSchema.title.ilike(f"%{search_keyword}%"),
                cast(RecipeSchema.ingredients, String).ilike(f"%{search_keyword}%")
            ))
        if not is_all and user_id:
            query = query.filter(RecipeSchema.created_by == user_id)
        query = query.order_by(RecipeSchema.id)
        total_count = select_count(query)
        query = query.limit(limit).offset((page - 1) * limit)
        query = select_all(query)
        return query, total_count
