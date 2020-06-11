from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from functools import lru_cache
import time

from config import conn_string
from models import Book, Availability

## TODO: Refactor into models.py and STANDARDISE NAMING (_db suffix)

def is_book_present(bid, user_id):
    return _get_book(bid, user_id) is not None

def get_book_title_details(bid, user_id):
    book = _get_book(bid, user_id)
    return { 'title': book.title, 'author': book.author }

def add_book_availabilities_db(bid, user_id, title_details, availability_info):
    if _get_book(bid, user_id):
        raise ValueError('Book with bid=%d and user_id=%d already exists' % (bid, user_id))
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

## Deletes a Book and its Availabilities, returning the deleted book's ID
def delete_book_and_availabilities(bid, user_id):
    if _get_book(bid, user_id) is None:
        raise LookupError('Book with bid=%d and user_id=%d does not exist' % (bid, user_id))
    book_id = _delete_book_cascade(bid, user_id)
    return book_id

## TODO: Temporary solution to list book information, just gives bids, titles, and authors for now. Modify as necessary
def get_book_info(user_id):
    books = _get_books_by_user_id(user_id)
    return [{ 'bid': book.bid, 'title': book.title, 'author': book.author } for book in books]

#####################
## PRIVATE METHODS ##
#####################

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

def _delete_book_cascade(bid, user_id):
    session = _create_session()
    book = _get_book(bid, user_id)
    book_id = book.id
    _delete_availabilities(book_id)
    session.delete(book)
    session.commit()
    session.close()
    return book_id

def _get_book(bid, user_id):
    session = _create_session()
    book = session.query(Book).filter(Book.bid == bid).filter(Book.user_id == user_id).first()
    session.close()
    return book

def _get_books_by_user_id(user_id):
    session = _create_session()
    books = session.query(Book).filter(Book.user_id == user_id).all()
    session.close()
    return books

## Creates an Availability, returning its ID
def _create_availability(book_id, branch_name, call_number, status_desc, shelf_location):
    session = _create_session()
    availability = Availability(
        book_id=book_id,
        branch_name=branch_name,
        call_number=call_number,
        status_desc=status_desc,
        shelf_location=shelf_location
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
