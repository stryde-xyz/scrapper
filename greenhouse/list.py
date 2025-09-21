import html
from time import sleep
import requests
from database import Job
from dateutil import parser
import html

class GreenHouseList:
    def __init__(self, companies, db):
        self._companies = companies
        self.db = db
        self.session = self.db.get_session()

    def start(self):
        while True:
            try:
                for company in self._companies:
                    self.process_company(company)
                    sleep(0.1)
            except Exception as e:
                print(f"Error processing {e}")


    def process_company(self, company):
        try:
            pages = 1
            response = requests.get(f'https://job-boards.greenhouse.io/embed/job_board?for={company}&page=1&_data=routes%2Fembed.job_board')
            if response.status_code == 200:
                pages = response.json()['jobPosts']['total_pages']

            for page in range(pages):
                print(f"Company: {company}, Page: {page+1}, Count: {response.json()['jobPosts']['total']}")
                response = requests.get(f'https://job-boards.greenhouse.io/embed/job_board?for={company}&page={page+1}&_data=routes%2Fembed.job_board')
                if response.status_code == 200:
                    internal_company = response.json()['board']['name']
                    for job in response.json()['jobPosts']['data']:
                        # print(job['id'])
                        # print(self.session.query(Job).filter_by(id=job['id']).first())
                        # print(parser.parse(job['published_at']))
                        if self.session.query(Job).filter_by(id=job['id']).first() is None:
                            # print(job)
                            published_at = parser.parse(job['published_at'])
                            updated_at = parser.parse(job['updated_at'])
                            html_content = html.unescape(job['content'])
                            # new_job = Job(job['id'], name=job['title'], internal_job_id=job['internal_job_id'],
                            #     published_at=published_at, updated_at=updated_at, apply_url=job['absolute_url'],
                            #     content=html_content, location=job['location'], company=company)

                            _job_to_add = Job(id=job['id'], name=job['title'], internal_job_id=job['id'], published_at=published_at,
                                updated_at=updated_at,  apply_url = job['absolute_url'],content = html_content, location = job['location'],
                                company = internal_company)

                            self.session.add(_job_to_add)


                            print(f"added job {job['id']}")
                        else:
                            # print(f"job exists {job['id']}")
                            pass
                    self.session.commit()
        except Exception as e:
            print(f"Error adding job {job['id']}: {e}")
