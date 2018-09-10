from .associations import roles_association
from cryptacular import bcrypt
from datetime import datetime as dt
from .meta import Base
from .role import AccountRole
from .preferences import Preferences
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
    DateTime,
)

manager = bcrypt.BCRYPTPasswordManager()

# Prior to adding preferences, stringify json. After retreiving, parse.


class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(Text, nullable=False)
    preferences = relationship(Preferences, back_populates='accounts')
    roles = relationship(AccountRole, secondary=roles_association, back_populates='accounts')

    date_created = Column(DateTime, default=dt.now())
    date_updated = Column(DateTime, default=dt.now(), onupdate=dt.now())

    def __init__(self, email, password=None):
        self.email = email
        self.password = manager.encode(password, 10)
        # self.preferences = preferences

    @classmethod
    def new(cls, request, email=None, password=None):
        """Register a new user
        """
        if not request.dbsession:
            raise DBAPIError

        user = cls(email, password)
        request.dbsession.add(user)

        # TODO: Assign roles to new user
        # This is unsafe!!!!
        admin_role = request.dbsession.query(AccountRole).filter(
            AccountRole.name == 'admin').one_or_none()

        user.roles.append(admin_role)
        request.dbsession.flush()

        return request.dbsession.query(cls).filter(
            cls.email == email).one_or_none()

    @classmethod
    def one(cls, request, email=None):
        return request.dbsession.query(cls).filter(
            cls.email == email).one_or_none()

    @classmethod
    def get_prefs(cls, request, email=None):
        return request.dbsession.query(cls).filter(
            cls.preferences == preferences).one_or_none()

    @classmethod
    def check_credentials(cls, request, email, password):
        """Validate that user exists and they are who they say they are
        """
        if request.dbsession is None:
            raise DBAPIError
        try:
            account = request.dbsession.query(cls).filter(
                cls.email == email).one_or_none()
        except DBAPIError:
            return None

        if account is not None:
            if manager.check(account.password, password):
                return account

        return None
