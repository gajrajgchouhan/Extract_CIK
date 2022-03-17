file = open(r"adobe_10q.txt", "r").read()
op = open("./parsed_forms/op_10q.txt", "w")

import re
import pandas as pd

def extract_items(part_header, part_text, form_type):
    """Extracts the item header and its corresponding text for every item within the plain text of a "part" of a form.
    
    :type part_header: str
    :param part_header: The header of a "part" of a form (e.g. Part III)
    
    :type part_text: str
    :param part_text: The plain text of a "part" of a form (e.g. Part III). In the case of 10-K and 8-K forms, the "part" is the whole form.
    
    :type form_type: str
    :param form_type: The form type (e.g. 10-K, 10-Q, 8-K)

    :rtype: Iterator[(str, str, str)]
    :returns: An iterator over tuples of the form (part_header, item_header, text) 
        where "item_header" is the item header and "text" is the corresponding text
        for each item in the "part". part_header is included to differentiate 
        between portions of a filing that have the same item number but are in different parts.
    """
    pattern = '(?P<header>(\n\n(ITEM|Item) \d+[A-Z]*.*?)\n\n)(?P<text>.*?)(?=(\n\n(ITEM|Item) \d+[A-Z]*.*?)\n\n|$)'
    return ((part_header, _.group('header').strip(), _.group('text').strip()) for _ in re.finditer(pattern, part_text, re.DOTALL))


def extract_parts(form_text, form_type):
    """Extracts every part from form plain text, where a "part" is defined
    specifically as a portion in the form starting with "PART (some roman numeral)".
    
    :type form_text: str
    :param form_text: The form plain text.
    
    :type form_type: str
    :param form_type: The form type (e.g. 10-K, 10-Q, 8-K)
    
    :rtype: Iterator[(str, str)]
    :returns: An iterator over the header and text for each part extracted from the form plain text.
        (e.g. for 10-K forms, we iterate through Part I through Part IV)
    """
    pattern = '((^PART|^Part|\n\nPART|\n\nPart) [IVXLCDM]+).*?(\n\n.*?)(?=\n\n(PART|Part) [IVXLCDM]+.*?\n\n|$)'
    return ((_.group(1).strip(), _.group(3)) for _ in re.finditer(pattern, form_text, re.DOTALL))

def get_form_items(form_text, form_type):
    """Extracts the item header and its corresponding text for every item within a form's plaintext.
    
    :type form_text: str
    :param form_text: The form plain text.
    
    :type form_type: str
    :param form_type: The form type (e.g. 10-K, 10-Q, 8-K)
    
    :rtype: Iterator[(str, str)]
    :returns: An iterator over tuples of the form (header, text) where "header" is the item header and "text" is the corresponding text.
    """
    
    for part_header, part_text in extract_parts(form_text, form_type):
        items = extract_items(part_header, part_text, form_type)
        yield from items

# got_form_items = get_form_items(file,"10-Q")

def items_to_df_row(item_iter, columns, form_type):
    """Takes an iterator over tuples of the form (header, text) that is created from calling extract_items
    and generates a row for a dataframe that has a column for each of the item types.
    
    :type item_iter: Iterator[(str, str, str)]
    :param item_iter: An iterator over tuples of the form (part_header, item_header, item_text).
    
    :type columns: List[str]
    :param columns: A list of column names for the dataframe we wish to generate a row for.
    
    :type form_type: str
    :param form_type: The form type. Currently supported types include 10-K, 10-Q, 8-K.
    
    :rtype: List[str]
    :returns: A row for the dataframe.
    """
    mapping = {} # mapping between processed column names and their corresponding row index
    for idx, col_name in enumerate(columns):
        processed_col_name = col_name.lower()
        mapping[processed_col_name] = idx
        
    returned_row = ["" for i in range(len(columns))]
    for part_header, item_header, text in item_iter:
        processed_header = (part_header.lower() + " " + item_header.lower()).strip()

        processed_header = re.search("part [ivxlcdm]+ item \d+[a-z]*", processed_header).group(0)

        if processed_header in mapping.keys():
            row_index = mapping[processed_header]
            returned_row[row_index] = text
            
    return returned_row

columns_10Q = ["Part I Item 1", "Part I Item 2", "Part I Item 3", "Part I Item 4",
               "Part II Item 1", "Part II Item 1A", "Part II Item 2", "Part II Item 3",
               "Part II Item 4", "Part II Item 5", "Part II Item 6"]
            
header_mappings_10Q = {
    "Part I Item 1": "Financial Statements",
    "Part I Item 2": "Management’s Discussion and Analysis of Financial Condition and Results of Operations",
    "Part I Item 3": "Quantitative and Qualitative Disclosures About Market Risk",
    "Part I Item 4": "Controls and Procedures",
    "Part II Item 1": "Legal Proceedings",
    "Part II Item 1A": "Risk Factors",
    "Part II Item 2": "Unregistered Sales of Equity Securities and Use of Proceeds",
    "Part II Item 3": "Defaults Upon Senior Securities",
    "Part II Item 4": "Mine Safety Disclosures",
    "Part II Item 5": "Other Information",
    "Part II Item 6": "Exhibits"
}                

def process_filings(dataframe, form_type):
    columns = columns_10Q
    header_mappings = header_mappings_10Q
        
    df = dataframe[dataframe.form_type == form_type]
    items = pd.DataFrame(columns = columns, dtype=object)
    for i in df.index:
        form_text = df.text[i]
        item_iter = get_form_items(form_text, form_type)
        items.loc[i] = items_to_df_row(item_iter, columns, form_type)
    items.rename(columns=header_mappings, inplace=True)
    df = pd.merge(df, items, left_index=True, right_index=True)
    return df

