# Setting Up the Python Env

- Install the requirements from `requirements.txt` using `pip3 install -r requirements.txt`. (Preferably in a virtual environment.)

# Downloading Data

- Run the `download_fillings.py` for dowloading the data.
- Download and run mongodb.
- Make sure its running at `127.0.0.1:27017`
- Then run the `populate_db.py` file to upload the cleaned data to the local mongodb service.

# Documentation for each file

- `download_filings.py` : This for the downloading the forms for companies given in the PS. It uses a csv file consisting of the CIK for these companies.
- `extract_cik.py` : This was used to find the CIK for all the companies given in PS. We found the list of the companies similiar to the given name, then used an string matching algorithm (from `difflib` module in python 3) to find the closest name and then took CIK of that name. Except 10-15 names all of the companies and the CIK were easily and accurately found. We added the remaining CIK manually in the sheet.
- `extract_ticker.py` : This was used for mapping the CIK to the tickers.
- `parse_10q.py`: This file consist of function for parsing the 10Q forms.
- `parse_form.py` : This file consist of function for parsing the 10K forms.
- `populate_db.py` : This will read the downloaded files and upload the cleaned dataset to mongodb.
