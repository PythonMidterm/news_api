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
from sqlalchemy import ARRAY

from .meta import Base


class Preferences(Base):
    __tablename__ = 'preferences'
    id = Column(Integer, primary_key=True)
    preference_order = Column(ARRAY(Text))
    date_created = Column(DateTime, default=dt.now())
    date_updated = Column(DateTime, default=dt.now(), onupdate=dt.now())
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    accounts = relationship('Account', back_populates='preferences')

    @classmethod
    def set_default(cls, request, **kwargs):
        """Method to create new user preferences in database
        """
        if request.dbsession is None:
            raise DBAPIError
        preferences = cls(**kwargs)

        request.dbsession.add(preferences)
        return request.dbsession.query(cls).filter(
            cls.account_id == kwargs['account_id']).one_or_none()

    @classmethod
    def update_prefs(cls, request, **kwargs):
        """Method to update user preferences in database by reassigning cls on 
        the correct account id column to the new preferences on the kwargs 
        coming in
        """
        if request.dbsession is None:
            raise DBAPIError

        prefs_to_update = request.dbsession.query(cls).filter(
            cls.account_id == kwargs['account_id']).first()

        prefs_to_update.preference_order = kwargs['preference_order']
        request.dbsession.flush()

        return request.dbsession.query(cls).filter(
            cls.account_id == kwargs['account_id']).one_or_none()

    @classmethod
    def one_by_account_id(cls, request=None, kwarg=None):
        """Method to retrieve user preferences by a single kwarg
        """
        if request.dbsession is None:
            raise DBAPIError
        return request.dbsession.query(cls).filter(
            cls.account_id == kwarg).one_or_none()
