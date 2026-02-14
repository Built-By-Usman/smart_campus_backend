from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL = "postgresql+psycopg2://postgres.spcohlicnsroxcfieipi:Shani.Malik321@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres?sslmode=require"

engine=create_engine(DATABASE_URL,poolclass=NullPool)

session_local=sessionmaker(autoflush=False,autocommit=False,bind=engine)

base=declarative_base()

def get_db():
    db=session_local()
    try:
        yield db
    finally:
        db.close()