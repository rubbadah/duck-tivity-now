from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from config import Config

config = Config()

engine = create_engine(
    config.database_url,
    # echo=True,
    pool_pre_ping=True,
)

Base = declarative_base()

Session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        Session.remove()
