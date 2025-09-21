from turtle import title
from urllib import parse

from sqlalchemy.sql.dml import UpdateDMLState
from sqlalchemy.sql.expression import Null
from database import Database, Job, OldJob
from os.path import join, dirname
from dotenv import load_dotenv
import os
import html
from dateutil import parser

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

database_url = os.getenv('DATABASE_URL')

db = Database(database_url)

session = db.get_session()

count = session.query(OldJob).count()
pages = count // 100

print(count)
print(pages)

try:
    for page in range(1, pages+1):
        old_jobs = session.query(OldJob).offset(page * 100).limit(100).all()
        for job in old_jobs:
            existin_job = session.query(Job).filter_by(id=job.id).first()
            print(existin_job)
            if existin_job is None:
                html_content = html.unescape(str(job.content))
                published_at = parser.parse(str(job.published_at))
                if job.published_at is Null:
                    published_at = parser.parse(str(job.updated_at))
                updated_at = parser.parse(str(job.updated_at))

                _job_to_add = Job(id=job.id, name=job.name, internal_job_id=job.internal_job_id, published_at=published_at,
                    updated_at=updated_at,  apply_url = job.apply_url, content = html_content, location = job.location,
                    company = job.company)

                session.add(_job_to_add)
                print(f"added {_job_to_add.id}")
                session.commit()

except Exception as e:
    print(e)
# OldJobs = session.query(OldJob).all()

# print(count)
