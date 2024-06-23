from sqlalchemy import or_
from sqlalchemy.orm import Session
from src.db.session import get_db, save_new_row, update_old_row, select_first
from src.schema.schema import UsersSchema
from src.utils.time import get_current_datetime

db: Session = get_db()


class UserModel:
    """Company Tracker Model"""

    @classmethod
    def create(cls, **kw):
        """method to save data in Company tracker"""
        obj = UsersSchema(**kw)
        obj.created_on = get_current_datetime()
        obj.updated_on = get_current_datetime()
        save_new_row(obj)
        return obj

    @classmethod
    def patch(cls, _id: int, **kw):
        """method to update user"""
        obj = db.query(UsersSchema).filter(UsersSchema.id == _id).first()
        for key, value in kw.items():
            setattr(obj, key, value)
        obj.updated_on = get_current_datetime()
        update_old_row(obj)
        return obj

    @classmethod
    def get_user_login(cls, email: str, mobile_no: str):
        """method to get user login"""
        query = db.query(UsersSchema).filter(
            or_(
                UsersSchema.email == email,
                UsersSchema.mobile_no == mobile_no
            )
        )
        return select_first(query)

    @classmethod
    def get_user(cls, email: str):
        """method to get user by email"""
        query = db.query(UsersSchema).filter(UsersSchema.email == email)
        query = select_first(query)
        return query
