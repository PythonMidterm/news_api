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
            cls.preference_order == kwargs['preference_order']).one_or_none()

