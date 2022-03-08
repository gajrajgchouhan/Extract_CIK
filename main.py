from time import time
import pandas as pd
from edgar import Edgar
import logging
from difflib import get_close_matches

logging.basicConfig(filename="main.py.log", level=logging.DEBUG)

startTime = int(time())
companyList = pd.read_csv("./Software-Company-List-v2.csv")
companyList["cik"] = None
companyList["findCompanies"] = None
companyList["closedCompany"] = None
edgar = Edgar()

logging.info("Starting to process the list of companies")
for index, company in enumerate(companyList.Company.values.flatten()):
    print(index, end="\r")
    logging.debug(company)
    try:
        possible_companies = edgar.find_company_name(company)
        closestCompany = get_close_matches(company, possible_companies, n=1)[0]
        companyList.iloc[index, 2] = str(possible_companies)
        companyList.iloc[index, 3] = closestCompany
        companyList.iloc[index, 1] = edgar.get_cik_by_company_name(closestCompany)
        companyList.to_csv(f"./output-{startTime}.csv", index=False)
    except Exception as e:
        logging.error(e)
        continue
