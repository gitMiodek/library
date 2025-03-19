from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, Query

from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
import app.models as models
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from starlette.responses import HTMLResponse
import app.schemas as schemas
from typing import Any


@asynccontextmanager
async def app_lifespan(app: FastAPI) -> Any:
    """
    Inicjalizacja tabel w bazie danych przy starcie aplikacji
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
async def add_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """
    Add book to the library
    """
    # Sprawdzenie, czy książka o podanym numerze seryjnym już istnieje
    db_book = db.query(models.Book).filter(models.Book.serial_number == book.serial_number).first()
    if db_book:
        raise HTTPException(status_code=400, detail="Book with the given serial number already exists!")

    # Sprawdzenie formatu numeru seryjnego (sześciocyfrowa liczba)
    if len(str(book.serial_number)) != 6:
        raise HTTPException(status_code=400, detail="The serial number must be a six-digit number")

    # Tworzenie nowego obiektu książki
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

# @app.delete("/delete_book/{serial_number}")

