import json
import re
import bleach
from tqdm.auto import tqdm
import html

# "backend/scraping/download_filings/sec-edgar-filings/0001023731/10-K/0001023731-19-000037/full-submission.txt"
# https://airccj.org/CSCP/vol7/csit76615.pdf


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
    # (r"<Table.*?</Table>", re.S | re.I),
    # (r"<[^>]*>", re.S),
]

patterns_for_remove = [re.compile(i, j) for i, j in patterns_for_remove]

# reading file
txt = open("./full-submission.txt", "r").read()

for pattern in tqdm(patterns_for_remove, desc="Remove document metadata", total=len(patterns_for_remove)):
    txt = re.sub(pattern, "", txt)

RE_S_I = re.S | re.I


def clean_unicode(txt):
    """
    Remove unnecessary tags, and clean unicode characters
    """
    txt = bleach.clean(txt, tags=["div", "table", "tr", "th", "td"], attributes=[], styles=[], strip=True)
    txt = re.sub(compile(r"&#\d+;", re.S | re.M), "", txt)
    txt = re.sub(compile(r"\\u[0-9a-fA-F]+", re.S | re.M), "", txt)
    return txt


# txt = html.unescape(txt)

# Renaming Item Heading
txt = re.sub(compile(r"> +Item|>Item|^Item", re.S | re.I | re.M), ">°Item", txt)
# removing extra spaces
txt = re.sub(compile(r"\t{2,}", re.S), "", txt)
txt = re.sub(compile(r" {2,}", re.S), "", txt)

final = {
    "Item 1": {"txt": re.findall(compile(r"°Item 1[^AB0-6].*?°Item", RE_S_I), txt)},
    "Item 1A": {"txt": re.findall(compile(r"°Item 1A.*?°Item", RE_S_I), txt)},
    "Item 1B": {"txt": re.findall(compile(r"°Item 1B.*?°Item", RE_S_I), txt)},
    "Item 2": {"txt": re.findall(compile(r"°Item 2.*?°Item", RE_S_I), txt)},
    "Item 3": {"txt": re.findall(compile(r"°Item 3.*?°Item", RE_S_I), txt)},
    "Item 4": {"txt": re.findall(compile(r"°Item 4.*?°Item", RE_S_I), txt)},
    "Item X": {"txt": re.findall(compile(r"°Item X.*?°Item", RE_S_I), txt)},
    "Item 5": {"txt": re.findall(compile(r"°Item 5.*?°Item", RE_S_I), txt)},
    "Item 6": {"txt": re.findall(compile(r"°Item 6.*?°Item", RE_S_I), txt)},
    "Item 7": {"txt": re.findall(compile(r"°Item 7[^A].*?°Item", RE_S_I), txt)},
    "Item 7A": {"txt": re.findall(compile(r"°Item 7A.*?°Item", RE_S_I), txt)},
    "Item 8": {"txt": re.findall(compile(r"°Item 8.*?°Item", RE_S_I), txt)},
    "Item 9": {"txt": re.findall(compile(r"°Item 9[^AB].*?°Item", RE_S_I), txt)},
    "Item 9A": {"txt": re.findall(compile(r"°Item 9A.*?°Item", RE_S_I), txt)},
    "Item 9B": {"txt": re.findall(compile(r"°Item 9B.*?°Item", RE_S_I), txt)},
    "Item 10": {"txt": re.findall(compile(r"°Item 10.*?°Item", RE_S_I), txt)},
    "Item 11": {"txt": re.findall(compile(r"°Item 11.*?°Item", RE_S_I), txt)},
    "Item 12": {"txt": re.findall(compile(r"°Item 12.*?°Item", RE_S_I), txt)},
    "Item 13": {"txt": re.findall(compile(r"°Item 13.*?°Item", RE_S_I), txt)},
    "Item 14": {"txt": re.findall(compile(r"°Item 14.*?(°Item|</TEXT>)", RE_S_I), txt)},
    "Item 15": {"txt": re.findall(compile(r"°Item 15.*?</TEXT>", RE_S_I), txt)},
}

json.dump(txt, open("test.txt", "w"), indent=4)

table_re = compile(r"<table>.*?</table>", RE_S_I)
for k, v in tqdm(final.items()):
    txt = v["txt"]
    v["table"] = []
    txt = [clean_unicode(i) for i in txt]

    for i in txt:
        v["table"].extend(re.findall(table_re, i))

    txt = [re.sub(table_re, "", i) for i in txt]

    final_txt = []
    for i in txt:
        final_txt.extend(re.split(r"<div>(.*?)</div>", i))
    v["txt"] = [i for i in final_txt if len(i) > 0]

json.dump(final, open("final_ara.json", "w"), indent=4)
