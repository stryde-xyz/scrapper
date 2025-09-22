import os
import sys
from os.path import join, dirname
import argparse
from database import Database
from greenhouse import load_csv
from smartrecruiter import SmartRecruiterAll
from greenhouse import GreenHouseList
from workable import WorkableAll
from dotenv import load_dotenv

def main(ats: str):
    database_url = os.getenv('DATABASE_URL')
    try:
        database = Database(database_url)
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)
    try:
        match ats:
            case 'smartrecruiters-all':
                smartrecruiter_all = SmartRecruiterAll(database)
                smartrecruiter_all.start()
            case 'smartrecruiters':
                print("Hello from scrapper!")
            case 'greenhouse':
                company_names = load_csv(f"{os.getcwd()}/greenhouse/companies.csv")
                greenhoouse_list = GreenHouseList(company_names, database)
                greenhoouse_list.start()
            case 'workable':
                workable_all = WorkableAll()
                workable_all.start()
            case _:
                print("Invalid ATS type")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrapper')

    parser.add_argument('ats_name', type=str, help='Choose a ATS type. smartrecruiters-all, smartrecruiters, personio, greenhouse, workable')
    args = parser.parse_args()

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    main(args.ats_name)
