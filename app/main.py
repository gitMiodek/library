from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

import app.models as models
import app.schemas as schemas
from app.database import engine, SessionLocal


@asynccontextmanager
async def app_lifespan(app: FastAPI) -> Any:
    """
    DB init during app startup
    """

    models.Base.metadata.create_all(bind=engine)
    yield


app: FastAPI = FastAPI(
    title="Library API",
    version="POC",
    description=open('app/info.md').read(),
    lifespan=app_lifespan
)


@app.get("/")
def home() -> None:
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/add_book", response_model=schemas.Book)
async def add_book(book: schemas.BookBase, db: Session = Depends(get_db)):
    """
    Add book to the library
    """
    if len(str(book.serial_number)) != 6:
        raise HTTPException(status_code=400, detail="The serial number must be a six-digit number")
    db_book = db.query(models.Book).filter(models.Book.serial_number == book.serial_number).first()
    if db_book:
        raise HTTPException(status_code=400, detail="Book with the given serial number already exists!")

    db_book = models.Book(
        serial_number=book.serial_number,
        title=book.title,
        author=book.author,
        is_borrowed=False
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@app.delete("/delete_book/{serial_number}")
async def del_book(serial_number: int, db: Session = Depends(get_db)) -> dict[str, str]:
    """
    Remove book from the library
    """
    if len(str(serial_number)) != 6:
        raise HTTPException(status_code=400, detail="The serial number must be a six-digit number")
    db_book = db.query(models.Book).filter(models.Book.serial_number == serial_number).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book with given serial number does not exist")
    db.delete(db_book)
    db.commit()
    return {"message": f"Book with serial number = {serial_number} has beed removed from the library"}


@app.get("/list_books", response_model=list[schemas.Book])
def list_books(db: Session = Depends(get_db)):
    """
    List books in the library
    """
    query = db.query(models.Book)

    books = query.all()
    return books


@app.put("/books/borrow/{serial_number}", response_model=schemas.Book)
def borrow_book(serial_number: int, db: Session = Depends(get_db)):
    """
    Update the book's state as borrowed
    """
    if len(str(serial_number)) != 6:
        raise HTTPException(status_code=400, detail="The serial number must be a six-digit number")
    db_book = db.query(models.Book).filter(models.Book.serial_number == serial_number).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book with given serial number does not exist")

    if db_book.is_borrowed:
        raise HTTPException(status_code=400, detail="Book is already borrowed")

    db_book.is_borrowed = True  # type: ignore
    db_book.borrowed_date = datetime.now()  # type: ignore

    db.commit()
    db.refresh(db_book)
    return db_book


@app.put("/books/return/{serial_number}", response_model=schemas.Book)
def return_book(serial_number: int, db: Session = Depends(get_db)):
    """
    Update the book's state as not borrowed
    """

    if len(str(serial_number)) != 6:
        raise HTTPException(status_code=400, detail="The serial number must be a six-digit number")
    db_book = db.query(models.Book).filter(models.Book.serial_number == serial_number).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book with given serial number does not exist")
    if not db_book.is_borrowed:
        raise HTTPException(status_code=400, detail="Book with given serial number is not borrowed")

    db_book.is_borrowed = False  # type: ignore
    db_book.borrowed_date = None  # type: ignore

    db.commit()
    db.refresh(db_book)
    return db_book
