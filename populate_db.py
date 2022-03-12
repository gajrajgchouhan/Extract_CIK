import os
from pathlib import Path
import re
import pandas as pd

from pymongo import MongoClient

client = MongoClient("127.0.0.1", 27017)
db = client["digital-alpha"]

"""
Collection names

1. companies
"""

# tickers: pd.DataFrame = pd.read_csv("./tickers.csv", dtype=str)[["Company", "cik", "tickers"]]
# db["companies"].insert_many(tickers.to_dict(orient="records"))

"""
2. filings
"""

# collection = db.collection_name
# folder_path = "download_filings/sec-edgar-filings"

# for path in Path(folder_path).glob("**/*.txt"):
#     pattern = rf"{folder_path}/(\d+)/(\d{{1,2}}-[QK])/(\d+-\d{{2}}-\d+)/full-submission.txt"
#     CIK, form_number, ASN = re.findall(pattern, str(path))[0]
#     print(CIK, form_number, ASN)
