"""common serializers"""
from pydantic import BaseModel
from typing import Optional


class Page(BaseModel):
    """Paging"""
    page_size: Optional[int] = 0
    page_number: Optional[int] = 0
    num_pages: Optional[int] = 0
    total_results: Optional[int] = 0


class SuccessResponsePartial(BaseModel):
    """Success Response with partial"""
    status: str = "success"
    message: Optional[str] = "Data saved successfully!"
    page: Optional[Page] = None
    data: Optional[dict] = {}
