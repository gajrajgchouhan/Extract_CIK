import re


def extract_numeric_para(section_dict):
    numeric_para = {}

    for section_name, v in section_dict.items():
        numeric_para[section_name] = {
            "text": [i for i in v["text"] if len(re.findall(r"\d+", i)) > 0],
            "table": v["table"],
        }
    return numeric_para
