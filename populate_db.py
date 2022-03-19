import logging
from pathlib import Path
import re
import pandas as pd

from pymongo import MongoClient
from pymongo.database import Database
from parse_form import parse_form
import parse_10q

client = MongoClient("127.0.0.1", 27017)
db: Database = client["digital-alpha"]

"""
Collection names
"""

"""
1. companies
"""

tickers: pd.DataFrame = pd.read_csv("./tickers.csv", dtype=str)[["Company", "cik", "tickers"]]
db.drop_collection("companies")
db.create_collection("companies")
db["companies"].insert_many(tickers.to_dict(orient="records"))

"""
2. filings
"""

db.drop_collection("fillings")
db.create_collection("fillings")

folder_path = "download_filings/sec-edgar-filings"
pattern_of_path = rf"{folder_path}/(\d+)/(\d{{1,2}}-[QK])/(\d+-\d{{2}}-\d+)/full-submission.txt"


for path in Path(folder_path).glob("**/*.txt"):
    CIK, form_number, ASN = re.findall(pattern_of_path, str(path))[0]
    logging.debug(f"{CIK}, {form_number}, {ASN}")
    filling_txt = open(path).read()
    if form_number == "10-Q":
        section_dict = parse_10q.parse_form(filling_txt)
    elif form_number == "10-K":
        section_dict = parse_form(filling_txt)
    else:
        continue

    db.fillings.update_one(
        {
            "cik": CIK,
        },
        {"$push": {"fillings": {"form_number": form_number, "asn": ASN, "parsed": section_dict}}},
        upsert=True,
    )
