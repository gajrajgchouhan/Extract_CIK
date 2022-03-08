import pandas as pd

mapper = pd.read_csv("./cik_ticker.csv", sep="|", dtype=str)
mapper["CIK"] = mapper.CIK.apply(lambda x: x.zfill(10))

CIKS: pd.DataFrame = pd.read_csv("./finalsheet.csv", dtype=str)
CIKS["tickers"] = None

for (index, *row) in CIKS.itertuples():
    print(index, end="\r")
    result = mapper[mapper.CIK == row[1]]
    if len(result) == 0:
        continue
    row[-1] = list(result.Ticker)[0]
    CIKS.iloc[index] = row

CIKS.to_csv("./tickers.csv", index=False)

# import numpy as np
# import pandas as pd
# from sec_cik_mapper import StockMapper

# mapper = StockMapper()

# CIKS: pd.DataFrame = pd.read_csv("./finalsheet.csv", dtype=str)
# CIKS["tickers"] = None

# for (index, *row) in CIKS.itertuples():
#     print(index, end="\r")
#     row[-1] = mapper.cik_to_tickers.get(row[1], None)
#     if row[-1] is not None and len(row[-1]) == 1:
#         row[-1] = list(row[-1])[0]
#     CIKS.iloc[index] = row

# CIKS.to_csv("./tickers.csv", index=False)
