from datetime import datetime as dt
from sqlalchemy.exc import DBAPIError
from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
)
from .meta import Base


class Feed(Base):
    __tablename__ = 'feed'
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    # description = Column(Text)
    url = Column(Text)
    dom_tone = Column(Text)
    date_created = Column(DateTime, default=dt.now())
    date_updated = Column(DateTime, default=dt.now(), onupdate=dt.now())

    def __init__(self, title=None, url=None, dom_tone=None):
        self.title = title
        self.url = url
        self.dom_tone = dom_tone

    @classmethod
    def new(cls, title=None, url=None, dom_tone=None):
        if not request.dbsession:
            raise DBAPIError

        article = cls(title, url, dom_tone)
        request.dbsession.add(article)

    @classmethod
    def get_all(cls, request):
        """Method to retrieve feed from database
        """
        if request.dbsession is None:
            raise DBAPIError

        # TODO: Research SQLAlchemy logic for grabbing everything from a table.
        return request.dbsession.query(cls).all()

    @classmethod
    def delete_all(cls):
        if not request.dbsession:
            raise DBAPIError
        return request.dbsession.query(cls).delete()
