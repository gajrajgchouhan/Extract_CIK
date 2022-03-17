import json
import re
import bleach
from tqdm.auto import tqdm
import os
import html

# "backend/scraping/download_filings/sec-edgar-filings/0001023731/10-K/0001023731-19-000037/full-submission.txt"
# https://airccj.org/CSCP/vol7/csit76615.pdf

txt = open("./full-submission.txt", "r").read()

patterns_for_extract = {
    "10-K": (r"<TYPE>10-K.*?</TEXT>", re.DOTALL),
}


def compile(p, f):
    return re.compile(p, f)


patterns_for_remove = [
    (r"<TYPE>GRAPHIC.*?</TEXT>", re.S),
    (r"<TYPE>EXCEL.*?</TEXT>", re.S),
    (r"<TYPE>PDF.*?</TEXT>", re.S),
    (r"<TYPE>ZIP.*?</TEXT>", re.S),
    (r"<TYPE>COVER.*?</TEXT>", re.S),
    (r"<TYPE>CORRESP.*?</TEXT>", re.S),
    (r"<TYPE>EX-10[01].INS.*?</TEXT>", re.S),
    (r"<TYPE>EX-99.SDR[KL].INS.*?</TEXT>", re.S),
    (r"<TYPE>EX-10[01].SCH.*?</TEXT>", re.S),
    (r"<TYPE>EX-99.SDR[KL].SCH.*?</TEXT>", re.S),
    (r"<TYPE>EX-10[01].CAL.*?</TEXT>", re.S),
    (r"<TYPE>EX-99.SDR[KL].CAL.*?</TEXT>", re.S),
    (r"<TYPE>EX-10[01].DEF.*?</TEXT>", re.S),
    (r"<TYPE>EX-99.SDR[KL].LAB.*?</TEXT>", re.S),
    (r"<TYPE>EX-10[01].LAB.*?</TEXT>", re.S),
    (r"<TYPE>EX-10[01].PRE.*?</TEXT>", re.S),
    (r"<TYPE>EX-99.SDR[KL].PRE.*?</TEXT>", re.S),
    (r"<TYPE>EX-10[01].REF.*?</TEXT>", re.S),
    (r"<TYPE>XML.*?</TEXT>", re.S),
    (r"<TYPE>.*", 0),
    (r"<SEQUENCE>.*", 0),
    (r"<FILENAME>.*", 0),
    (r"<DESCRIPTION>.*", 0),
    (r"<HEAD>.*?</HEAD>", re.S),
    (r"<Table.*?</Table>", re.S | re.I),
    (r"<[^>]*>", re.S),
]

patterns_for_remove = [re.compile(i, j) for i, j in patterns_for_remove]

for pattern in tqdm(patterns_for_remove, total=len(patterns_for_remove)):
    txt = re.sub(pattern, " ", txt)

# txt = html.unescape(txt)
cleaner = bleach.Cleaner(tags=["table", "tr", "td"], attributes=[], styles=[], strip=True)
txt = cleaner.clean(txt)
txt = re.sub(compile(r"> +Item|>Item|^Item", re.S | re.I | re.M), "Item", txt)
txt = re.sub(compile(r"\s{2,}", re.S), " ", txt)
txt = re.sub(r"&#\d+;", " ", txt)

final = {
    "Item 1": {"txt": re.findall(compile(r"Item 1[^AB0-5].*?Item", re.S | re.I), txt)},
    "Item 1A": {"txt": re.findall(compile(r"Item 1A.*?Item", re.S | re.I), txt)},
    "Item 1B": {"txt": re.findall(compile(r"Item 1B.*?Item", re.S | re.I), txt)},
    "Item 2": {"txt": re.findall(compile(r"Item 2.*?Item", re.S | re.I), txt)},
    "Item 3": {"txt": re.findall(compile(r"Item 3.*?Item", re.S | re.I), txt)},
    "Item 4": {"txt": re.findall(compile(r"Item 4.*?Item", re.S | re.I), txt)},
    "Item X": {"txt": re.findall(compile(r"Item X.*?Item", re.S | re.I), txt)},
    "Item 5": {"txt": re.findall(compile(r"Item 5.*?Item", re.S | re.I), txt)},
    "Item 6": {"txt": re.findall(compile(r"Item 6.*?Item", re.S | re.I), txt)},
    "Item 7": {"txt": re.findall(compile(r"Item 7[^A].*?Item", re.S | re.I), txt)},
    "Item 7A": {"txt": re.findall(compile(r"Item 7A.*?Item", re.S | re.I), txt)},
    "Item 8": {"txt": re.findall(compile(r"Item 8.*?Item", re.S | re.I), txt)},
    "Item 9": {"txt": re.findall(compile(r"Item 9[^AB].*?Item", re.S | re.I), txt)},
    "Item 9A": {"txt": re.findall(compile(r"Item 9A.*?Item", re.S | re.I), txt)},
    "Item 9B": {"txt": re.findall(compile(r"Item 9B.*?Item", re.S | re.I), txt)},
    "Item 10": {"txt": re.findall(compile(r"Item 10.*?Item", re.S | re.I), txt)},
    "Item 11": {"txt": re.findall(compile(r"Item 11.*?Item", re.S | re.I), txt)},
    "Item 12": {"txt": re.findall(compile(r"Item 12.*?Item", re.S | re.I), txt)},
    "Item 13": {"txt": re.findall(compile(r"Item 13.*?Item", re.S | re.I), txt)},
    "Item 14": {"txt": re.findall(compile(r"Item 14.*?(Item|</TEXT>)", re.S | re.I), txt)},
    "Item 15": {"txt": re.findall(compile(r"Item 14.*?</TEXT>", re.S | re.I), txt)},
}

file = open("./customer_data/8X8.txt", "w")
pattern = re.compile(r"([a-ZA-Z]){100}%([a-ZA-Z]){100}")


table_re = re.compile(r"<table>.*?</table>", re.S | re.I)
for k, v in tqdm(final.items()):
    print(k)
    print(type(v), "\n")
    # exit()
    txt = " ".join(v["txt"])
    v["table"] = re.findall(table_re, txt)
    v["txt"] = re.sub(compile(r"<[^>]*>", re.S), "", txt)

json.dump(final, open("final_ara.json", "w"), indent=4)

# table_re = re.compile(r"<table>.*?</table>", re.S | re.I)
# for k, v in tqdm(final.items()):
#     txt = " ".join(v["txt"])
#     v["table"] = re.findall(table_re, txt)
#     v["txt"] = re.sub(compile(r"<[^>]*>", re.S), "", txt)

# json.dump(final, open("final_ara.json", "w"), indent=4)
