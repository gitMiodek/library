from pydantic import BaseModel, conint
from datetime import datetime
from typing import Optional

class BookBase(BaseModel):
    """
    Podstawowy schemat książki
    """
    serial_number: int
    title: str
    author: str

class BookCreate(BookBase):
    """
    Schemat do tworzenia nowej książki
    """
    pass

class Book(BookBase):
    """
    Pełny schemat książki zwracany przez API
    """
    is_borrowed: bool
    borrowed_date: Optional[datetime] = None
    borrower_id: Optional[int] = None

    class Config:
        orm_mode = True

class BorrowInfo(BaseModel):
    """
    Schemat informacji o wypożyczeniu
    """
    borrower_id: int

class Message(BaseModel):
    """
    Schemat wiadomości
    """
    message: str