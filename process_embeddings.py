from typing import Dict, List

import json
import math
import openai
import os
import random
import time
import threading

import chromadb
from concurrent.futures import ThreadPoolExecutor, as_completed
import sqlite3
from tenacity import (
    retry,
    stop_after_attempt,
    wait_fixed,
)
import tqdm

from topics import TOPICS


data_folder = '/Users/johnmorris/arxiv-gpt/data/'

# maintain separate databases for papers and topics. makes it easier
# to regenerate one or the other.
data_conn = sqlite3.connect(os.path.join(data_folder, 'database.db'), check_same_thread=False)
data_cursor = data_conn.cursor()

conn = sqlite3.connect(os.path.join(data_folder, 'topics.db'), check_same_thread=False)
cursor = conn.cursor()

lock = threading.Lock()

# table 3: topics
cursor.execute('''CREATE TABLE IF NOT EXISTS topics
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   topic TEXT,
                   paper_id TEXT)''')


@retry(wait=wait_fixed(1), stop=stop_after_attempt(10))
def embed(text_list_batch, model):
    return openai.Embedding.create(
            input=text_list_batch,
            model=model,
            encoding_format="float",  # override default base64 encoding...
        )

def get_embeddings_openai_vanilla(text_list, model="text-embedding-ada-002") -> list:
    # embeddings model: https://platform.openai.com/docs/guides/embeddings/use-cases
    #    api ref: https://platform.openai.com/docs/api-reference/embeddings/create
    # TODO: set up a caching system somehow.
    import openai
    # print(f"running openai on text_list of length {len(text_list)}, first element '{text_list[0]}'")
    batches = math.ceil(len(text_list) / 128)
    outputs = []
    for batch in tqdm.trange(batches):
        text_list_batch = text_list[batch * 128 : (batch + 1) * 128]
        response = embed(text_list_batch, model)
        outputs.extend([e["embedding"] for e in response["data"]])
    return outputs


def main():
    client = chromadb.Client(
        chromadb.config.Settings(
            persist_directory="data/.chroma",
            chroma_db_impl='duckdb+parquet',
        )
    )
    collection = client.get_or_create_collection("embeddings")

    # pull all documents
    # Get 5 random documents
    data_cursor.execute("SELECT * FROM documents")
    documents = data_cursor.fetchall()
    document_ids, _dates, document_data = map(list, zip(*documents)) # reshape
    document_data = list(map(json.loads, document_data))

    documents_to_embed = [f"Title: {d['title']}\nAbstract: {d['abstract'][:500]}..." for d in document_data]
    embeddings = get_embeddings_openai_vanilla(documents_to_embed)

    collection.add(
        embeddings=embeddings,
        metadatas=[{ "id": d["id"], "title": d["title"]} for d in document_data],
        documents=documents_to_embed,
        ids=list(map(str, document_ids)),
    )
    client.persist()
            
    conn.close()
    print(f"done :-) (added {len(embeddings)} embeddings); total {collection.count()}")


if __name__ == '__main__':
    main()