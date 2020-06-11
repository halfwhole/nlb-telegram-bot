from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from config import conn_string

Base = declarative_base()

## NOTE: A potential source of confusion is the difference between Book's id and bid.
## - Book's id is the primary key assigned by this database.
## - Book's bid is that which is used to identify NLB books, as per the catalogue URL.
## - Availability's book_id refers to the Book's id, not bid.

class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    bid = Column(Integer)
    user_id = Column(Integer)
    title = Column(String(200))
    author = Column(String(200))
    availabilities = relationship('Availability', backref='book')

    @staticmethod
    def get(bid, user_id):
        session = _create_session()
        book = session.query(Book).filter(Book.bid == bid).filter(Book.user_id == user_id).first()
        session.close()
        return book

    # Gets all books with the given user_id
    @staticmethod
    def get_all(user_id):
        session = _create_session()
        books = session.query(Book).filter(Book.user_id == user_id).all()
        session.close()
        return books

    @staticmethod
    def create(bid, user_id, title, author):
        session = _create_session()
        book = Book(bid=bid, user_id=user_id, title=title, author=author)
        session.add(book)
        session.commit()
        book_id = book.id
        session.close()
        return book_id

    @staticmethod
    def delete_cascade(bid, user_id):
        session = _create_session()
        book = Book.get(bid, user_id)
        book_id = book.id
        Availability.delete_all(book_id)
        session.delete(book)
        session.commit()
        session.close()
        return book_id

    def __repr__(self):
        return "<Book(id=%s, bid=%d, user_id=%d, title='%s', author='%s')" % (
            self.id, self.bid, self.user_id, self.title, self.author)


class Availability(Base):
    __tablename__ = 'availability'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('book.id'))
    branch_name = Column(String(200))
    call_number = Column(String(200))
    status_desc = Column(String(200))
    shelf_location = Column(String(200))

    @staticmethod
    def create(book_id, branch_name, call_number, status_desc, shelf_location):
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

    ## Deletes all Availabilities referencing the given book id
    @staticmethod
    def delete_all(book_id):
        session = _create_session()
        availabilities = session.query(Availability).filter(Availability.book_id == book_id).all()
        for availability in availabilities:
            session.delete(availability)
        session.commit()
        session.close()

    def __repr__(self):
        return "<Availability(id=%s, book_id=%d, branch_name='%s', status_desc='%s')" % (
            self.id, self.book_id, self.branch_name, self.status_desc)


## Remember to call session.close() after you finish!
def _create_session():
    engine = create_engine(conn_string)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


if __name__ == '__main__':
    session = _create_session()
