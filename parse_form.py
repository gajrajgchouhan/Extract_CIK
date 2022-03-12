import json
import re
import bleach
from tqdm.auto import tqdm
import html

# "backend/scraping/download_filings/sec-edgar-filings/0001023731/10-K/0001023731-19-000037/full-submission.txt"
# https://airccj.org/CSCP/vol7/csit76615.pdf

RE_S_I = re.S | re.I


def compile(p, f):
    return re.compile(p, f)


def clean_unicode(txt):
    """
    Remove unnecessary tags, and clean unicode characters

    bleach.clean only keeps the allowed tags and removes everything else (including css)
    then remove any unicode chars
    """
    txt = bleach.clean(txt, tags=["div", "table", "tr", "th", "td"], attributes=[], styles=[], strip=True)
    txt = re.sub(compile(r"&#\d+;", re.S | re.M), "", txt)
    txt = re.sub(compile(r"\\u[0-9a-fA-F]+", re.S | re.M), "", txt)
    return txt


# patterns for removing the metadata
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
filling_txt = open("./full-submission.txt", "r").read()

for pattern in tqdm(patterns_for_remove, desc="Remove document metadata", total=len(patterns_for_remove)):
    filling_txt = re.sub(pattern, "", filling_txt)

# Renaming Item Heading
filling_txt = re.sub(compile(r"> +Item|>Item|^Item", re.S | re.I | re.M), ">°Item", filling_txt)

# removing extra spaces
filling_txt = re.sub(compile(r"\t{2,}", re.S), "", filling_txt)
filling_txt = re.sub(compile(r" {2,}", re.S), "", filling_txt)

section_dict = {
    "Item 1": {"text": re.findall(compile(r"°Item 1[^AB0-6].*?°Item", RE_S_I), filling_txt)},
    "Item 1A": {"text": re.findall(compile(r"°Item 1A.*?°Item", RE_S_I), filling_txt)},
    "Item 1B": {"text": re.findall(compile(r"°Item 1B.*?°Item", RE_S_I), filling_txt)},
    "Item 2": {"text": re.findall(compile(r"°Item 2.*?°Item", RE_S_I), filling_txt)},
    "Item 3": {"text": re.findall(compile(r"°Item 3.*?°Item", RE_S_I), filling_txt)},
    "Item 4": {"text": re.findall(compile(r"°Item 4.*?°Item", RE_S_I), filling_txt)},
    "Item X": {"text": re.findall(compile(r"°Item X.*?°Item", RE_S_I), filling_txt)},
    "Item 5": {"text": re.findall(compile(r"°Item 5.*?°Item", RE_S_I), filling_txt)},
    "Item 6": {"text": re.findall(compile(r"°Item 6.*?°Item", RE_S_I), filling_txt)},
    "Item 7": {"text": re.findall(compile(r"°Item 7[^A].*?°Item", RE_S_I), filling_txt)},
    "Item 7A": {"text": re.findall(compile(r"°Item 7A.*?°Item", RE_S_I), filling_txt)},
    "Item 8": {"text": re.findall(compile(r"°Item 8.*?°Item", RE_S_I), filling_txt)},
    "Item 9": {"text": re.findall(compile(r"°Item 9[^AB].*?°Item", RE_S_I), filling_txt)},
    "Item 9A": {"text": re.findall(compile(r"°Item 9A.*?°Item", RE_S_I), filling_txt)},
    "Item 9B": {"text": re.findall(compile(r"°Item 9B.*?°Item", RE_S_I), filling_txt)},
    "Item 10": {"text": re.findall(compile(r"°Item 10.*?°Item", RE_S_I), filling_txt)},
    "Item 11": {"text": re.findall(compile(r"°Item 11.*?°Item", RE_S_I), filling_txt)},
    "Item 12": {"text": re.findall(compile(r"°Item 12.*?°Item", RE_S_I), filling_txt)},
    "Item 13": {"text": re.findall(compile(r"°Item 13.*?°Item", RE_S_I), filling_txt)},
    "Item 14": {"text": re.findall(compile(r"°Item 14.*?(°Item|</TEXT>)", RE_S_I), filling_txt)},
    # "Item 15": {"text": re.findall(compile(r"°Item 15.*?</TEXT>", RE_S_I), filling_txt)},
}
# item 15 is not necessary for now and it keeps conflicting with item 1

# json.dump(txt, open("test.txt", "w"), indent=4)

pattern_for_extract_table = compile(r"<table>.*?</table>", RE_S_I)
for section_name, section_txt in tqdm(section_dict.items()):
    if len(section_txt["text"]) > 0:
        # the zeroth index matches with the table of contents! which is not needed
        section_txt["text"] = [section_txt["text"][1]]
    text = section_txt["text"]
    section_txt["table"] = []
    text = [clean_unicode(i) for i in text]

    # extracting tables
    for i in text:
        section_txt["table"].extend(re.findall(pattern_for_extract_table, i))

    # remove the tables from text
    text = [re.sub(pattern_for_extract_table, "", i) for i in text]

    # splitting the text to paragraphs by using divs
    final_text = []
    for i in text:
        final_text.extend(re.split(r"<div>(.*?)</div>", i))

    # ignore small text
    section_txt["text"] = [i for i in final_text if len(i) > 30]

json.dump(section_dict, open("final_ara.json", "w"), indent=4)
