import json
import re

section_dict = json.load(open("./final_ara.json"))


def extract_numeric_para(section_dict):
    numeric_para = {}

    for section_name, v in section_dict.items():
        numeric_para[section_name] = [i for i in v["text"] if len(re.findall(r"\d+", i)) > 0]
    return numeric_para
