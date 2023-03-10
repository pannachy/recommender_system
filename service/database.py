from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

'''
генератор сессий
'''


SQLALCHEMY_DATABASE_URL = "postgresql://user:password@host:dbname"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)    #, pool_size=10, max_overflow=0, pool_timeout=60
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

