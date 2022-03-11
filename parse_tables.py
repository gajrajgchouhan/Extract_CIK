import json

sections = json.load(open("./final_ara.json"))

for _, v in sections.items():
    if len(v["table"]) > 0:
        print(len(v["table"]))
