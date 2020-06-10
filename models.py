from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

## https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/basic_use.html

Base = declarative_base()

class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    bid = Column(Integer)
    user_id = Column(Integer)
    title = Column(String(200))
    author = Column(String(200))
    availabilities = relationship('Availability', backref='book')

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

    def __repr__(self):
        return "<Availability(id=%s, book_id=%d, branch_name='%s', status_desc='%s')" % (
            self.id, self.book_id, self.branch_name, self.status_desc)

if __name__ == '__main__':
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from config import conn_string
    engine = create_engine(conn_string)
    Session = sessionmaker(bind=engine)
    session = Session()
