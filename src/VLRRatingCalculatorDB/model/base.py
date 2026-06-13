"""SQLAlchemy declarative base shared by every ORM model in the package."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """SQLAlchemy declarative base used by all ORM models in the package."""

