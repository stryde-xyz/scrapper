from sqlalchemy import create_engine, Column, BigInteger, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
# NewBase = declarative_base()

class Database:
    def __init__(self, url):
        self._db_engine = create_engine(url)
        Base.metadata.create_all(self._db_engine)
        # NewBase.metadata.create_all(self._db_engine)
        session = sessionmaker(bind=self._db_engine)
        self._db_session = session()
        print("Database created")


    def get_engine(self):
        return self._db_engine

    def get_session(self):
        return self._db_session

class Job(Base):
    __tablename__ = 'job_v1'

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    internal_job_id = Column(BigInteger)
    published_at = Column(DateTime)
    updated_at = Column(DateTime)
    apply_url = Column(String)
    content = Column(String)
    location = Column(String)
    company = Column(String)

    def __repr__(self):
        return f"Job(id={self.id}, name={self.name}, internal_job_id={self.internal_job_id}, published_at={self.published_at}, updated_at={self.updated_at}, apply_url={self.apply_url}, content={self.content}, location={self.location}, company={self.company})"

# class NewJob(NewBase):
#     __tablename__ = "new_jobs"

#     id = Column(BigInteger, primary_key=True)
#     name = Column(String)
#     internal_job_id = Column(BigInteger)
#     published_at = Column(DateTime)
#     updated_at = Column(DateTime)
#     apply_url = Column(String)
#     content = Column(String)
#     location = Column(String)
#     company = Column(String)
