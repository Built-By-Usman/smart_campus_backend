from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL="postgresql://usman:ShaniMalik321@localhost:5432/smart_campus_management_system"

engine=create_engine(DATABASE_URL)

session_local=sessionmaker(autoflush=False,autocommit=False,bind=engine)

base=declarative_base()

def get_db():
    db=session_local()
    try:
        yield db
    finally:
        db.close()