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
    description = Column(Text)
    url = Column(Text)
    date_created = Column(DateTime, default=dt.now())
    date_updated = Column(DateTime, default=dt.now(), onupdate=dt.now())

    @classmethod
    def get_all(cls, request):
        """Method to retrieve feed from database
        """
        if request.dbsession is None:
            raise DBAPIError

        # Research SQLAlchemy logic for grabbing everything from a table.
        return request.dbsession.query(cls).filter(
            cls.symbol == kwargs['symbol']).one_or_none()


