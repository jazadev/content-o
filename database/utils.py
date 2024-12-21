"""Call and configuration Flask extensions.
"""
from datetime import datetime, UTC
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_migrate import Migrate

names_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata_obj = MetaData(naming_convention=names_convention)

class Base(DeclarativeBase):
    """Class to Set General Definitions."""
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now(UTC),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=datetime.now(UTC),
        nullable=True
    )
# Create instance of SQLAlchemy class
db = SQLAlchemy(model_class=Base, metadata=metadata_obj)
migrate = Migrate()
