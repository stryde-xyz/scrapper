import html
from time import sleep
import requests
from database import Job

class GreenHouseList:
    def __init__(self, companies, db):
        self._companies = companies
        self.db = db
        self.session = self.db.get_session()

    def start(self):
        while True:
            for company in self._companies:
                self.process_company(company)
                sleep(0.1)


    def process_company(self, company):
        try:
            pages = 1
            response = requests.get(f'https://job-boards.greenhouse.io/embed/job_board?for={company}&page=1&_data=routes%2Fembed.job_board')
            if response.status_code == 200:
                pages = response.json()['jobPosts']['total_pages']

            for page in range(pages):
                print(f"Company: {company}, Page: {page+1}")
                if page != 0:
                    response = requests.get(f'https://job-boards.greenhouse.io/embed/job_board?for={company}&page={page+1}&_data=routes%2Fembed.job_board')
                    if response.status_code == 200:
                        for job in response.json()['jobPosts']['data']:
                            existing_job = self.session.query(Job).filter_by(id=job['id']).first()
                            if existing_job is None:
                                self.session.add(Job(id=job['id'], name=job['title'], internal_job_id = job['internal_job_id'], published_at=job['published_at'],
                                updated_at = job['updated_at'], apply_url=job['absolute_url'], content=job['content'], location=job['location'], company=company))
                                # print(f"added job {job['id']}")
                            else:
                                # print(f"job exists {job['id']}")
                                pass
            self.session.commit()

        except Exception as e:
            print(f"Error occured {e}")
