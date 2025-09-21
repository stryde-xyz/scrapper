import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, BigInteger, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Database:
    def __init__(self, url):
        self._db_engine = create_engine(url)
        Base.metadata.create_all(self._db_engine)
        session = sessionmaker(bind=self._db_engine)
        self._db_session = session()
        print("Database created")


    def get_engine(self):
        return self._db_engine

    def get_session(self):
        return self._db_session



class Job(Base):
    __tablename__ = 'jobs'

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    internal_job_id = Column(BigInteger)
    published_at = Column(String)
    updated_at = Column(String)
    apply_url = Column(String)
    content = Column(String)
    location = Column(String)
    company = Column(String)
