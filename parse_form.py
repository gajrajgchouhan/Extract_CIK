import json
import re
from tqdm.auto import tqdm
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
    txt = re.sub(pattern, "", txt)

txt = html.unescape(txt)
txt = re.sub(compile(r"> +Item|>Item|^Item", re.S | re.I | re.M), "Item", txt)
txt = re.sub(compile(r"\s{2,}", re.S), "", txt)

final = {
    "Item 1": (re.findall(compile(r"Item 1[^AB0-5].*?Item", re.S | re.I), txt)),
    "Item 1A": (re.findall(compile(r"Item 1A.*?Item", re.S | re.I), txt)),
    "Item 1B": (re.findall(compile(r"Item 1B.*?Item", re.S | re.I), txt)),
    "Item 2": (re.findall(compile(r"Item 2.*?Item", re.S | re.I), txt)),
    "Item 3": (re.findall(compile(r"Item 3.*?Item", re.S | re.I), txt)),
    "Item 4": (re.findall(compile(r"Item 4.*?Item", re.S | re.I), txt)),
    "Item X": (re.findall(compile(r"Item X.*?Item", re.S | re.I), txt)),
    "Item 5": (re.findall(compile(r"Item 5.*?Item", re.S | re.I), txt)),
    "Item 6": (re.findall(compile(r"Item 6.*?Item", re.S | re.I), txt)),
    "Item 7": (re.findall(compile(r"Item 7[^A].*?Item", re.S | re.I), txt)),
    "Item 7A": (re.findall(compile(r"Item 7A.*?Item", re.S | re.I), txt)),
    "Item 8": (re.findall(compile(r"Item 8.*?Item", re.S | re.I), txt)),
    "Item 9": (re.findall(compile(r"Item 9[^AB].*?Item", re.S | re.I), txt)),
    "Item 9A": (re.findall(compile(r"Item 9A.*?Item", re.S | re.I), txt)),
    "Item 9B": (re.findall(compile(r"Item 9B.*?Item", re.S | re.I), txt)),
    "Item 10": (re.findall(compile(r"Item 10.*?Item", re.S | re.I), txt)),
    "Item 11": (re.findall(compile(r"Item 11.*?Item", re.S | re.I), txt)),
    "Item 12": (re.findall(compile(r"Item 12.*?Item", re.S | re.I), txt)),
    "Item 13": (re.findall(compile(r"Item 13.*?Item", re.S | re.I), txt)),
    "Item 14": (re.findall(compile(r"Item 14.*?(Item|</TEXT>)", re.S | re.I), txt)),
    "Item 15": (re.findall(compile(r"Item 14.*?</TEXT>", re.S | re.I), txt)),
}

json.dump(final, open("final_ara.json", "w"), indent=4)
