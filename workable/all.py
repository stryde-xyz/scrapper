from os import getcwd
from database import Job
import xml.etree.ElementTree as ET

class WorkableAll:
    def __init__(self):
        self.jobs = []

    def download_file(self, url):
        pass

    def open_xml(self, path):
        tree = ET.parse(f'{getcwd()}/workable.xml')
        root = tree.getroot()
        return root

    def process_jobs(self, xml):
        for job in xml.findall('job'):
            id = str(job.find('referencenumber').text).strip()
            title = str(job.find('title').text).strip()
            published_at = str(job.find('date').text).strip()
            company = str(job.find('company').text).strip()
            content = str(job.find('content').text).strip()
            location = str(job.find('city').text).strip()
            print(f"ID: {id}, Title: {title}, Company: {company}, Content: {content}, Location: {location}")

    def start(self):
        # self.download_file("https://www.workable.com/boards/workable.xml")
        xml = self.open_xml(getcwd())
        self.process_jobs(xml)
