import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """- Пользователи"""

    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    surname = sa.Column(sa.String, nullable=False)
    middle_name = sa.Column(sa.String, nullable=True)
    email = sa.Column(sa.String, unique=True)
    password = sa.Column(sa.String, nullable=True)
    created_date = sa.Column(sa.DateTime, server_default=func.now())
    updated_date = sa.Column(sa.DateTime, server_default=func.now(), onupdate=func.now())
