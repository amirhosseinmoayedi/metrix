from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.settings import settings


def get_session():
    engine = create_engine(settings.test_db_url)
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return session_local()
