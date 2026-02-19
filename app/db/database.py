from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.declarative import declarative_base
import os 
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL=os.getenv("DATABASE_URL")

engine=create_engine(DATABASE_URL,poolclass=NullPool)

session_local=sessionmaker(autoflush=False,autocommit=False,bind=engine)

base=declarative_base()

def get_db():
    db=session_local()
    try:
        yield db
    finally:
        db.close()