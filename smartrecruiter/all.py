import re
import requests
import hashlib
import json
from database import Job
from time import sleep

class SmartRecruiterAll:
    def __init__(self, db):
        self._prev_jobs = []
        self._jobs_string = ""
        self._prev_hash = None
        self._job_to_add = None
        self.jobs = []
        self.db = db
        self.session = self.db.get_session()

    def start(self):
        while True:

            if self.get_jobs():
                for job in self.jobs:
                    # print(job['id'])
                    try:
                        if not job['id'] in self._prev_jobs:
                            if self.get_job(job['id'], job['actions']['details']):
                                if not self.session.query(Job).filter_by(id=job['id']).first():
                                    # print(f"Job added: {job['id']}")
                                    self.session.add(self._job_to_add)
                                    self.session.commit()
                    except Exception as e:
                        print(f"❌ An error occurred: {e}")

            self._prev_jobs = [job['id'] for job in self.jobs]


            sleep(60)

    def get_job(self, job_id, api_url):
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                # print(data)
                html_content =  f"""
                <div>{data['jobAd']['sections']['companyDescription']['title']}</div>
                {data['jobAd']['sections']['companyDescription']['text']}
                <div>{data['jobAd']['sections']['jobDescription']['title']}</div>
                {data['jobAd']['sections']['jobDescription']['text']}
                <div>{data['jobAd']['sections']['qualifications']['title']}</div>
                {data['jobAd']['sections']['qualifications']['text']}
                <div>{data['jobAd']['sections']['additionalInformation']['title']}</div>
                {data['jobAd']['sections']['additionalInformation']['text']}
                """
                self._job_to_add = Job(id=job_id, name=data['name'], internal_job_id=data['id'], published_at=data['releasedDate'],
                    updated_at=data['releasedDate'],  apply_url = data['postingUrl'],content = html_content, location = data['location']['city'],
                    company = data['company']['name'])
                return True
            else:
                print(f"❌ Failed to retrieve job details: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Failed to retrieve job details: {e}")
            return False

    def get_jobs(self):
        try:
            response = requests.get('https://jobs.smartrecruiters.com/sr-jobs/search?limit=100')

            if response.status_code !=200:
                print(f"❌ Failed to retrieve job list: {response.status_code}")
                return False

            text = response.text

            hash = hashlib.sha256(text.encode()).hexdigest()

            if hash != self._prev_hash:
                self._prev_hash = hash
                self.jobs = [job for job in response.json()['content']]
                return True

        except requests.exceptions.RequestException as e:
            print(f"❌ An error occurred during the request: {e}")
        except json.JSONDecodeError as e:
            print(f"❌ Failed to decode JSON response: {e}")
        except KeyError as e:
            print(f"❌ Missing key in JSON data: {e}")


        return False
