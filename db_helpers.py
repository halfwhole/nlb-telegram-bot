from models import Book, Availability
from nlb import get_availability_info

def is_book_present(bid, user_id):
    return Book.get(bid, user_id) is not None

def get_book_title_details(bid, user_id):
    book = Book.get(bid, user_id)
    return { 'title': book.title, 'author': book.author }

def get_all_book_info(user_id):
    def make_book_info(book):
        return {
            'is_available': _is_book_available(book.id),
            'id': book.id,
            'bid': book.bid,
            'title': book.title,
            'author': book.author
        }
    books = Book.get_all(user_id)
    return [make_book_info(book) for book in books]

def add_book_availabilities(bid, user_id, title_details, availability_info):
    if Book.get(bid, user_id):
        raise ValueError('Book with bid=%d and user_id=%d already exists' % (bid, user_id))
    title = title_details['title']
    author = title_details['author']
    book_id = Book.create(bid, user_id, title, author)
    _update_availabilities(book_id, availability_info)

def delete_book_and_availabilities(bid, user_id):
    if Book.get(bid, user_id) is None:
        raise LookupError('Book with bid=%d and user_id=%d does not exist' % (bid, user_id))
    book_id = Book.delete_cascade(bid, user_id)
    return book_id

def refresh_all_availabilities(user_id):
    all_book_info = get_all_book_info(user_id)
    ## TODO: make this async
    book_ids_availability_infos = [(bi['id'], get_availability_info(bi['bid'])) for bi in all_book_info]
    for book_id, availability_info in book_ids_availability_infos:
        _update_availabilities(book_id, availability_info)

## Update Availabilities by deleting all existing ones, and creating again
def _update_availabilities(book_id, availability_info):
    Availability.delete_all(book_id)
    for availability in availability_info:
        branch_name = availability['branch_name']
        call_number = availability['call_number']
        status_desc = availability['status_desc']
        shelf_location = availability['shelf_location']
        Availability.create(book_id, branch_name, call_number, status_desc, shelf_location)


def _is_book_available(book_id):
    ## Returns if the book is available in ANY library
    availabilities = Availability.get_all_by_book_id(book_id)
    return any(availability.status_desc.strip().upper() == 'AVAILABLE' for availability in availabilities)
