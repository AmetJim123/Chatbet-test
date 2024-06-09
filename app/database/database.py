from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://root:Test_Password@localhost:3306/chatbet_test_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
meta = MetaData()

def get_db():
    """
    Returns a database session.

    This function creates a new session using the SessionLocal object and the configured database engine.
    The session is used to interact with the database and perform CRUD operations.

    Returns:
        db (SessionLocal): A database session object.

    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
