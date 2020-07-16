from pathos.pools import ProcessPool

from app.config import logger
from app.constants import LOG_ADD_MESSAGE_FORMAT, LOG_DELETE_MESSAGE_FORMAT, LOG_REFRESH_MESSAGE_FORMAT
from app.models import Book, Availability, Filter
from app.nlb import get_availability_info

CHECK_AVAILABLE_STRING = 'AVAILABLE'
BOOK_ALREADY_EXISTS_FORMAT = 'Book with bid=%d and user_id=%d already exists'
BOOK_DOES_NOT_EXIST_FORMAT = 'Book with bid=%d and user_id=%d does not exist'

###############################
## BOOK/AVAILABILITY HELPERS ##
###############################

def is_book_present(bid, user_id):
    return Book.get(bid, user_id) is not None

def get_book_title_details(bid, user_id):
    book = Book.get(bid, user_id)
    if not book:
        raise LookupError(BOOK_DOES_NOT_EXIST_FORMAT % (bid, user_id))
    return { 'title': book.title, 'author': book.author }

def get_book_availabilities(bid, user_id):
    def make_availability(availability):
        return {
            'is_available': _is_status_desc_available(availability.status_desc),
            'branch_name': availability.branch_name,
            'call_number': availability.call_number,
            'status_desc': availability.status_desc,
            'shelf_location': availability.shelf_location
        }
    book_id = Book.get(bid, user_id).id
    availabilities = Availability.get_all_by_book_id(book_id)
    return [make_availability(availability) for availability in availabilities]

def get_all_book_info(user_id):
    ## Returns if the book is available in FILTERED libraries
    def is_book_available(availabilities, filter_branch_names):
        if filter_branch_names:
            return any(_is_status_desc_available(a.status_desc) for a in availabilities if a.branch_name in filter_branch_names)
        else:
            return any(_is_status_desc_available(a.status_desc) for a in availabilities)
    def make_book_info(book, filter_branch_names):
        availabilities = Availability.get_all_by_book_id(book.id)
        return {
            'is_available': is_book_available(availabilities, filter_branch_names),
            'id': book.id,
            'bid': book.bid,
            'title': book.title,
            'author': book.author,
            'availabilities': availabilities
        }
    books = Book.get_all(user_id)
    filter_branch_names = get_filter_branch_names(user_id)
    return [make_book_info(book, filter_branch_names) for book in books]

def get_all_branch_names(user_id):
    all_book_info = get_all_book_info(user_id)
    all_availabilities = [bi['availabilities'] for bi in all_book_info]
    all_availabilities = [x for availability in all_availabilities for x in availability]
    branch_names = sorted(list(set(availability.branch_name for availability in all_availabilities)))
    return branch_names

def add_book_availabilities(bid, user_id, title_details, availability_info):
    if Book.get(bid, user_id):
        raise ValueError(BOOK_ALREADY_EXISTS_FORMAT % (bid, user_id))
    logger.info(LOG_ADD_MESSAGE_FORMAT % (user_id, bid))
    title = title_details['title']
    author = title_details['author']
    book_id = Book.create(bid, user_id, title, author)
    _update_availabilities(book_id, availability_info)

def delete_book_and_availabilities(bid, user_id):
    logger.info(LOG_DELETE_MESSAGE_FORMAT % (user_id, bid))
    if Book.get(bid, user_id) is None:
        raise LookupError(BOOK_DOES_NOT_EXIST_FORMAT % (bid, user_id))
    book_id = Book.delete_cascade(bid, user_id)
    return book_id

def refresh_all_availabilities(user_id):
    logger.info(LOG_REFRESH_MESSAGE_FORMAT % user_id)
    all_book_info = get_all_book_info(user_id)
    with ProcessPool(nodes=8) as pool:
        book_ids_availability_infos = pool.map(lambda bi: (bi['id'], get_availability_info(bi['bid'])), all_book_info)
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

def _is_status_desc_available(status_desc):
    return status_desc.strip().upper() == CHECK_AVAILABLE_STRING


####################
## FILTER HELPERS ##
####################

def get_filter_branch_names(user_id):
    filters = Filter.get_all(user_id)
    branch_names = sorted(filter.branch_name for filter in filters)
    return branch_names

def delete_all_filters(user_id):
    Filter.delete_all(user_id)

def delete_hanging_filters(user_id):
    branch_names = get_all_branch_names(user_id)
    filters = Filter.get_all(user_id)
    for filter in filters:
        if filter.branch_name not in branch_names:
            Filter.delete(user_id, filter.branch_name)

def toggle_filter(user_id, branch_name):
    filter = Filter.get(user_id, branch_name)
    if filter:
        Filter.delete(user_id, branch_name)
    else:
        Filter.create(user_id, branch_name)
