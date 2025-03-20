from pathlib import Path
import requests
import json

example_input_dir = Path(__file__).resolve().parents[1] / 'app/examples'


def test_add_book(port: int):
    response = requests.post(f"http://0.0.0.0:{port}/add_book",
                             json=json.load(open(example_input_dir / "book.json", 'r')))

    assert response.status_code == 200
    assert response.json()["serial_number"] == 123456
    assert response.json()["title"] == "A brief history of time"
    assert response.json()["author"] == "Stephen Hawking"


def test_add_book_with_invalid_serial_number(port: int):
    book_data = {"serial_number": 12345, "title": "Book Title", "author": "Author Name"}

    response = requests.post(f"http://0.0.0.0:{port}/add_book", json=book_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "The serial number must be a six-digit number"


def test_list_books(port: int):
    response = requests.get(f"http://0.0.0.0:{port}/list_books")

    assert response.status_code == 200
    books = response.json()
    assert len(books) == 1
    assert books[0]["title"] == "A brief history of time"


def test_borrow_book(port: int):
    response = requests.put(f"http://0.0.0.0:{port}/books/borrow/123456")

    assert response.status_code == 200
    assert response.json()["is_borrowed"] is True


def test_borrow_book_that_is_already_borrowed(port: int):
    # Attempting to borrow it again
    response = requests.put(f"http://0.0.0.0:{port}/books/borrow/123456")

    assert response.status_code == 400
    assert response.json()["detail"] == "Book is already borrowed"


def test_return_book(port: int):
    # Returning the book
    response = requests.put(f"http://0.0.0.0:{port}/books/return/123456")

    assert response.status_code == 200
    assert response.json()["is_borrowed"] is False


def test_return_book_that_is_not_borrowed(port: int):
    # Attempting to return a book that isn't borrowed
    response = requests.put(f"http://0.0.0.0:{port}/books/return/123456")

    assert response.status_code == 400
    assert response.json()["detail"] == "Book with given serial number is not borrowed"


def test_add_book_that_already_exists(port: int):
    response = requests.post(f"http://0.0.0.0:{port}/add_book",
                             json=json.load(open(example_input_dir / "book.json", 'r')))

    assert response.status_code == 400
    assert response.json()["detail"] == "Book with the given serial number already exists!"


def test_delete_book(port: int):
    response = requests.delete(f"http://0.0.0.0:{port}/delete_book/123456")

    assert response.status_code == 200
    assert response.json() == {"message": "Book with serial number = 123456 has beed removed from the library"}


def test_delete_non_existent_book(port: int):
    response = requests.delete(f"http://0.0.0.0:{port}/delete_book/123456")

    assert response.status_code == 404
    assert response.json()["detail"] == "Book with given serial number does not exist"
