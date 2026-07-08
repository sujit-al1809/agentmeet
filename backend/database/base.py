from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class every SQLAlchemy model inherits from.

    Alembic later imports this so it can discover all tables.
    """

    pass
