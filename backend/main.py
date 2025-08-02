from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from elasticsearch import Elasticsearch
from pydantic import BaseModel
from typing import List
import hashlib

# FastAPI App Setup
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Elasticsearch Config
es = Elasticsearch("http://localhost:9200")
INDEX_NAME = "rvce"

# Search Result Schema
class SearchResult(BaseModel):
    title: str
    url: str
    score: float
    snippet: str

# Helper: Normalize and hash text for fast deduplication
def normalize(text: str) -> str:
    return ''.join(e.lower() for e in text if e.isalnum() or e.isspace()).strip()

def hash_text(text: str) -> str:
    return hashlib.md5(normalize(text).encode("utf-8")).hexdigest()

# Search Endpoint
@app.get("/search", response_model=dict)
def search(query: str = Query(..., min_length=1)):
    response = es.search(index=INDEX_NAME, body={
        "size": 50,  # Limit for performance
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title^2", "content"],
                "fuzziness": "AUTO"
            }
        },
        "highlight": {
            "fields": {
                "content": {},
                "title": {}
            },
            "fragment_size": 150,
            "number_of_fragments": 1
        }
    })

    hits = response.get("hits", {}).get("hits", [])
    results = []
    seen_hashes = set()

    for hit in hits:
        source = hit["_source"]
        highlight = hit.get("highlight", {})
        snippet = highlight.get("content", highlight.get("title", [""]))[0] if highlight else source.get("content", "")[:150]

        title = source.get("title", "")
        combined = f"{title} {snippet}"
        doc_hash = hash_text(combined)

        if doc_hash in seen_hashes:
            continue

        seen_hashes.add(doc_hash)
        results.append({
            "title": title,
            "url": source.get("url", ""),
            "score": hit["_score"],
            "snippet": snippet
        })

    return {
        "query": query,
        "total": len(results),
        "results": results
    }
