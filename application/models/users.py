from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """- Пользователи"""

    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    surname = sa.Column(sa.String, nullable=False)
    middle_name = sa.Column(sa.String, nullable=False)
    email = sa.Column(sa.String, unique=True, nullable=False)
    password = sa.Column(sa.String, nullable=False)
    created_date = sa.Column(sa.DateTime(timezone=True), default=datetime.now(), nullable=True)
    updated_date = sa.Column(sa.DateTime(timezone=True), default=datetime.now(), nullable=True)
