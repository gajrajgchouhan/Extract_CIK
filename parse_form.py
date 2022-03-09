import re
from tqdm.auto import tqdm

# "backend/scraping/download_filings/sec-edgar-filings/0001023731/10-K/0001023731-19-000037/full-submission.txt"

txt = open("./full-submission.txt", "r").read()

patterns = [
    r"<TYPE>GRAPHIC.*?</TEXT>",
    r"<TYPE>EXCEL.*?</TEXT>",
    r"<TYPE>PDF.*?</TEXT>",
    r"<TYPE>ZIP.*?</TEXT>",
    r"<TYPE>COVER.*?</TEXT>",
    r"<TYPE>CORRESP.*?</TEXT>",
    r"<TYPE>EX-10[01].INS.*?</TEXT>",
    r"<TYPE>EX-99.SDR[KL].INS.*?</TEXT>",
    r"<TYPE>EX-10[01].SCH.*?</TEXT>",
    r"<TYPE>EX-99.SDR[KL].SCH.*?</TEXT>",
    r"<TYPE>EX-10[01].CAL.*?</TEXT>",
    r"<TYPE>EX-99.SDR[KL].CAL.*?</TEXT>",
    r"<TYPE>EX-10[01].DEF.*?</TEXT>",
    r"<TYPE>EX-99.SDR[KL].LAB.*?</TEXT>",
    r"<TYPE>EX-10[01].LAB.*?</TEXT>",
    r"<TYPE>EX-10[01].PRE.*?</TEXT>",
    r"<TYPE>EX-99.SDR[KL].PRE.*?</TEXT>",
    r"<TYPE>EX-10[01].REF.*?</TEXT>",
    r"<TYPE>XML.*?</TEXT>",
]

patterns = [re.compile(i, re.DOTALL) for i in patterns]

for pattern in tqdm(patterns, total=len(patterns)):
    txt = re.sub(pattern, "", txt)

with open("./test.txt", "w") as f:
    f.write(txt)
