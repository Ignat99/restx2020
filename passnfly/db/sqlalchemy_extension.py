from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

db = SQLAlchemy(
    metadata=MetaData(
        naming_convention={
            # Именование первичных ключей
            "pk": "pk_%(table_name)s",
            # Именование внешних ключей
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            # Именование индексов
            "ix": "ix_%(table_name)s_%(column_0_name)s",
            # Именование уникальных индексов
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            # Именование CHECK-constraint-ов
            "ck": "ck_%(table_name)s_%(constraint_name)s",
        }
    )
)
