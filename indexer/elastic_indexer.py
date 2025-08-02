import os
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

# Config
ES_HOST = "http://localhost:9200"
INDEX_NAME = "rvce"
DATA_FILE = "data/rvce_pages_with_pdfs.json"
FAILED_DOCS_FILE = "failed_docs.json"

# Connect
es = Elasticsearch(ES_HOST)

def connect_elasticsearch():
    if es.ping():
        print("[INFO] Connected to Elasticsearch.")
    else:
        raise ValueError("[ERROR] Could not connect to Elasticsearch.")

def create_index(index_name):
    if es.indices.exists(index=index_name):
        print(f"[INFO] Index '{index_name}' already exists. Deleting it...")
        es.indices.delete(index=index_name)
    print(f"[INFO] Creating index '{index_name}'...")
    index_config = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "url": {"type": "keyword"},
                "title": {"type": "text"},
                "content": {"type": "text"},
                "file_path": {"type": "keyword"},
                "department": {"type": "keyword"}  # ✅ new field added
            }
        }
    }
    es.indices.create(index=index_name, body=index_config)

def load_documents():
    with open(DATA_FILE, "r") as f:
        documents = json.load(f)
    print(f"[INFO] Loaded {len(documents)} documents from {DATA_FILE}")
    return documents

def index_documents_individually(docs):
    success, failed_docs = 0, []
    for i, doc in enumerate(docs):
        try:
            es.index(index=INDEX_NAME, id=i, document=doc)
            success += 1
        except Exception as e:
            failed_docs.append(doc)
    return success, failed_docs

if __name__ == "__main__":
    connect_elasticsearch()
    create_index(INDEX_NAME)

    docs = load_documents()
    success, failed_docs = index_documents_individually(docs)

    print(f"[INFO] Successfully indexed {success} documents.")
    if failed_docs:
        with open(FAILED_DOCS_FILE, "w") as f:
            json.dump(failed_docs, f, indent=2)
        print(f"[ERROR] {len(failed_docs)} document(s) failed and were saved to '{FAILED_DOCS_FILE}'.")

    print(f"[DONE] Indexed {success} out of {len(docs)} documents into '{INDEX_NAME}'")
