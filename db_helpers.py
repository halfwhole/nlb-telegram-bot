from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from functools import lru_cache
import time

from config import conn_string
from models import Book, Availability

def is_book_present(bid, user_id):
    return _get_book(bid, user_id) is not None

def add_book_availabilities_db(bid, user_id, title_details, availability_info):
    if _get_book(bid, user_id):
        raise ValueError('Book already exists')
    title = title_details['title']
    author = title_details['author']
    book_id = _create_book(bid, user_id, title, author)
    refresh_availabilities_db(book_id, availability_info)

def refresh_availabilities_db(book_id, availability_info):
    _delete_availabilities(book_id)
    for availability in availability_info:
        branch_name = availability['branch_name']
        call_number = availability['call_number']
        status_desc = availability['status_desc']
        shelf_location = availability['shelf_location']
        _create_availability(book_id, branch_name, call_number, status_desc, shelf_location)

## Remember to call session.close() after you finish!
def _create_session():
    engine = create_engine(conn_string)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

## Creates a Book, returning its ID
def _create_book(bid, user_id, title, author):
    session = _create_session()
    book = Book(bid=bid, user_id=user_id, title=title, author=author)
    session.add(book)
    session.commit()
    book_id = book.id
    session.close()
    return book_id

def _get_book(bid, user_id):
    session = _create_session()
    book = session.query(Book).filter(Book.bid == bid).filter(Book.user_id == user_id).first()
    session.close()
    return book

## Creates an Availability, returning its ID
def _create_availability(book_id, branch_name, call_number, status_desc, shelf_location):
    session = _create_session()
    availability = Availability(
        book_id=book_id,
        branch_name=branch_name,
        call_number=call_number,
        status_desc=status_desc
    )
    session.add(availability)
    session.commit()
    availability_id = availability.id
    session.close()
    return availability_id

## Deletes all Availabilities referencing the book_id
def _delete_availabilities(book_id):
    session = _create_session()
    availabilities = session.query(Availability).filter(Availability.book_id == book_id).all()
    for availability in availabilities:
        session.delete(availability)
    session.commit()
    session.close()
