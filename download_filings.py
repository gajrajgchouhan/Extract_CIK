import logging
import pandas as pd
from sec_edgar_downloader import Downloader
import os
from tqdm.auto import tqdm
import shutil

logging.basicConfig(filename="download_fillings.log", level=logging.DEBUG)

try:
    shutil.rmtree("./download_filings")
except Exception as e:
    print(e)

os.makedirs("./download_filings", exist_ok=False)

CIKS: pd.DataFrame = pd.read_csv("./finalsheet.csv", dtype=str)

dl = Downloader("./download_filings")
FORMS = ["10-K", "10-Q"]

for (index, *row) in tqdm(CIKS.iterrows(), total=len(CIKS), desc="Downloading filings"):
    if pd.isnull([row[0][1]]):
        continue
    logging.debug((row[0][0], "started"))
    for form in tqdm(FORMS, total=len(FORMS), desc="Downloading forms", leave=False):
        logging.debug(
            (
                "Downloaded",
                dl.get(form, row[0][1], after="2019-01-01", include_amends=False, download_details=False),
                "fillings",
            )
        )
    logging.debug((row[0][0], "completed"))
