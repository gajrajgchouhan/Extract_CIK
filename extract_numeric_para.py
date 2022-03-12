import json
import re

section_dict = json.load(open("./final_ara.json"))
numeric_para = {}

for section_name, v in section_dict.items():
    numeric_para[section_name] = [i for i in v["text"] if len(re.findall(r"\d+", i)) > 0]


with open("./numeric_para.json", "w") as f:
    json.dump(numeric_para, f, indent=4)
