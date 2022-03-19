import re
import re
import bleach
from tqdm.auto import tqdm
import logging

logging.basicConfig(filename="extract_numeric_para.log", level=logging.DEBUG)
RE_S_I = re.S | re.I

columns_10Q = [
    "Part I Item 1",
    "Part I Item 2",
    "Part I Item 3",
    "Part I Item 4",
    "Part II Item 1",
    "Part II Item 1A",
    "Part II Item 2",
    "Part II Item 3",
    "Part II Item 4",
    "Part II Item 5",
    "Part II Item 6",
]

header_mappings_10Q = {
    "Part I Item 1": "Financial Statements",
    "Part I Item 2": "Management's Discussion and Analysis of Financial Condition and Results of Operations",
    "Part I Item 3": "Quantitative and Qualitative Disclosures About Market Risk",
    "Part I Item 4": "Controls and Procedures",
    "Part II Item 1": "Legal Proceedings",
    "Part II Item 1A": "Risk Factors",
    "Part II Item 2": "Unregistered Sales of Equity Securities and Use of Proceeds",
    "Part II Item 3": "Defaults Upon Senior Securities",
    "Part II Item 4": "Mine Safety Disclosures",
    "Part II Item 5": "Other Information",
    "Part II Item 6": "Exhibits",
}


def compile(p, f=0):
    return re.compile(p, f)


# patterns for removing the metadata
PATTERNS_FOR_REMOVE = [
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
]

PATTERNS_FOR_REMOVE = [re.compile(i, j) for i, j in PATTERNS_FOR_REMOVE]


def parse_form(filling_txt: str):
    filling_txt = re.findall(r"<TYPE>10-Q.*?</TEXT>", filling_txt, re.S)
    filling_txt = filling_txt[0]

    for pattern in tqdm(PATTERNS_FOR_REMOVE, desc="Remove document metadata", total=len(PATTERNS_FOR_REMOVE)):
        filling_txt = re.sub(pattern, "", filling_txt)

    # removing extra spaces
    filling_txt = re.sub(compile(r"&nbsp;", re.S), "", filling_txt)
    filling_txt = re.sub(compile(r"&#\d+;", re.S | re.M), "", filling_txt)
    filling_txt = re.sub(compile(r"\\u[0-9a-fA-F]+", re.S | re.M), "", filling_txt)
    filling_txt = re.sub(compile(r"&rsquo;"), "'", filling_txt)
    filling_txt = re.sub(compile(r"&ldquo;"), "'", filling_txt)
    filling_txt = re.sub(compile(r"&rdquo;"), "'", filling_txt)
    filling_txt = bleach.clean(filling_txt, tags=["p", "div"], attributes=[], styles=["*"], strip=True)
    filling_txt = re.sub(compile(r"\s+"), " ", filling_txt)

    filling_txt = re.findall(
        r">\s*Item 2\s*.*?DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS(.*?)>\s*Item 3",
        filling_txt,
        re.S | re.I | re.M,
    )

    if len(filling_txt) == 0:
        return []

    filling_txt = filling_txt[0]
    filling_txt = [filling_txt.replace("<p>", "<div>").replace("</p>", "</div>")]

    # splitting the text to paragraphs by using divs
    final_text = []
    for i in filling_txt:
        final_text.extend(re.split(r"<div>(.*?)</div>", i))
    return [i for i in final_text if len(i) > 30]
