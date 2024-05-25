from config.config import setting
from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


def get_base() -> declarative_base:
    return Base


def get_session() -> sessionmaker:
    engine = get_engine()
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_engine() -> Engine:
    engine = create_engine(setting.DatabaseURL, connect_args={"check_same_thread": False}, echo=True)
    return engine


def get_db():
    db = get_session()()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    get_base().metadata.create_all(bind=get_engine())
