from datetime import datetime as dt
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
)
from sqlalchemy import ForeignKey

from .meta import Base


# Re-factor everything below
class Preferences(Base):
    __tablename__ = 'preferences'
    id = Column(Integer, primary_key=True)
    preference_order = Column(Text)
    date_created = Column(DateTime, default=dt.now())
    date_updated = Column(DateTime, default=dt.now(), onupdate=dt.now())
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    accounts = relationship('Account', back_populates='preferences')

    @classmethod
    def new(cls, request, **kwargs):
        """Method to create new user preferences in database
        """
        if request.dbsession is None:
            raise DBAPIError
        preferences = cls(**kwargs)
        request.dbsession.add(preferences)

        return request.dbsession.query(cls).filter(
            cls.preferences == kwargs['preference_order']).one_or_none()

    @classmethod
    def one(cls, request=None, pk=None):
        """Method to retrieve a portfolio by primary key
        """
        if request.dbsession is None:
            raise DBAPIError
        return request.dbsession.query(cls).get(pk)

    @classmethod
    def oneByKwarg(cls, request=None, kwarg=None):
        """Method to retrieve a portfolio by a single kwarg
        """
        if request.dbsession is None:
            raise DBAPIError
        return request.dbsession.query(cls).filter(
            cls.account_id == kwarg).one_or_none()
