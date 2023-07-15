from typing import Any, Dict, List

import json
import logging
import os
import sqlite3
import sys

import tqdm


logger = logging.getLogger('arxiv-gpt-data-pipeline')
logger.setLevel(logging.INFO)

ACCEPTABLE_CATEGORIES = {"cs.LG", "cs.AI", "cs.CL"}

# chatGPT gave me the following code which makes logging stuff
# print to the console. (why doesn't it print to console by default?)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
logger.addHandler(handler)

# database.
data_folder = '/Users/johnmorris/arxiv-gpt/data/'
conn = sqlite3.connect(os.path.join(data_folder, 'database.db'))
cursor = conn.cursor()

# table 1: documents
cursor.execute('''CREATE TABLE IF NOT EXISTS documents
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE,
                    data JSON)''')

# table 2: author names
cursor.execute('''CREATE TABLE IF NOT EXISTS authors
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT)''')


def load_data() -> List[Dict[str, Any]]:
    # data from here: https://www.kaggle.com/datasets/Cornell-University/arxiv?resource=download
    # filename = os.path.join(data_folder, 'arxiv-metadata-oai-snapshot-tiny.json')
    filename = os.path.join(data_folder, 'arxiv-metadata-oai-snapshot.json')
    logging.info("processing file %s", filename)
    lines = open(filename).readlines()
    return [json.loads(line) for line in tqdm.tqdm(lines, desc="processing lines", leave=False)]

def main():
    raw_data = load_data()

    ## 1. filter data. Only want CS/ML/NLP papers. also get author names.
    data = []
    authors = []
    for d in tqdm.tqdm(raw_data, desc="filtering"):
        categories = set(d["categories"].split())
        if len(categories & ACCEPTABLE_CATEGORIES) > 0:
            data.append(d)
            authors.extend(["__".join(a) for a in d["authors_parsed"]])


    print(len(data))
    logger.info("filtered data from %d to %d papers.", len(raw_data), len(data))

    # 2. extract all authors and save to elasticsearch.
    for author_name in tqdm.tqdm(authors, "writing authors to sqlite"):
        cursor.execute("INSERT OR IGNORE INTO authors (name) VALUES (?)",
                   (author_name,))

    # 3. store full docs in elasticsearch.
    for obj in tqdm.tqdm(data, desc="writing data to sqlite"):
        cursor.execute("INSERT INTO documents (date, data) VALUES (?,?)", (obj["update_date"], json.dumps(obj),))
    
    conn.commit()
    conn.close()
    logging.info("done :-)")

if __name__ == '__main__': main()