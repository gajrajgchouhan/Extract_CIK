import json
import pandas as pd

sections = json.load(open("./final_ara.json"))

for _, v in sections.items():
    if len(v["table"]) > 0:
        for table in v["table"]:
            print(pd.read_html(table))
    break
