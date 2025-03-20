import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

example_input_dir = Path(__file__).resolve().parents[1] / 'app/examples'


class BookBase(BaseModel):
    """
    Book schema
    """
    serial_number: int
    title: str
    author: str

    class Config:
        with open(example_input_dir / "book.json") as f:
            json_schema_extra = {'example': json.load(f)}


class Book(BookBase):
    """
    Book schema returned by API
    """
    is_borrowed: bool
    borrowed_date: Optional[datetime] = None

    class Config:
        from_attributes = True
