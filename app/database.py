from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import os


SQL_ALCHEMY_URL=f'postgresql://{settings.database_username}:{settings.database_pswrd}@{settings.database_hostname}:{settings.database_portname}/{settings.database_name}'
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"sslmode": "require"}
    )
else:
    engine = create_engine(SQL_ALCHEMY_URL)


SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()