import warnings
import numpy as np
import pandas as pd
from sec_edgar_downloader import Downloader
import os
from pathlib import Path
from tqdm.auto import tqdm
import shutil

try:
    shutil.rmtree("./download_filings")
except Exception as e:
    print(e)

os.makedirs("./download_filings", exist_ok=False)

CIKS: pd.DataFrame = pd.read_csv("./finalsheet.csv", dtype=str)

dl = Downloader("./download_filings")
FORMS = ["10-K", "10-Q", "8-K"]

for (index, *row) in tqdm(CIKS.iterrows(), total=len(CIKS), desc="Downloading filings"):
    if pd.isnull([row[0][1]]):
        continue
    for form in tqdm(FORMS, total=len(FORMS), desc="Downloading forms", leave=False):
        dl.get(form, row[0][1], after="2017-01-01", include_amends=False)
    break
