from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.database import Base


class Book(Base):
    """
    Model książki w bazie danych
    """
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(Integer, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    is_borrowed = Column(Boolean, default=False)
    borrowed_date = Column(DateTime, nullable=True)
    borrower_id = Column(Integer, nullable=True)
