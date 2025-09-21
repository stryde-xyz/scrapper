from greenhouse.list import GreenHouseList
import pandas as pd

def load_csv(file_path):
    df = pd.read_csv(file_path, header=None)
    df.columns = ["company_name"]
    company_name = [data for data in df["company_name"]]
    return company_name
