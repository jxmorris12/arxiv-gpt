from typing import Any, Dict, List

import json
import logging
import sys

import tqdm


logger = logging.getLogger('arxiv-gpt-data-pipeline')
logger.setLevel(logging.INFO)

# chatGPT gave me the following code which makes logging stuff
# print to the console. (why doesn't it print to console by default?)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
logger.addHandler(handler)


def load_data() -> List[Dict[str, Any]]:
    filename = "/Users/johnmorris/arxiv-gpt/data/arxiv-metadata-oai-snapshot-small.json"
    # filename = "/Users/johnmorris/arxiv-gpt/data/arxiv-metadata-oai-snapshot.json"
    logging.info("processing file %s", filename)
    lines = open(filename).readlines()
    return [json.loads(line) for line in tqdm.tqdm(lines, desc="processing lines", leave=False)]

def main():
    raw_data = load_data()

    ## 1. filter data. Only want CS/ML papers.
    data = []
    for d in tqdm.tqdm(raw_data, desc="filtering"):
        categories = d["categories"].split()
        if "cs.LG" in categories:
            data.append(d)


    print(len(data))
    logger.info("filtered data from %d to %d papers.", len(raw_data), len(data))

    ## 2. extract all authors and save to elasticsearch.
    # 3. store in elasticsearch.
    # for 

if __name__ == '__main__': main()