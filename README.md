# 🔍 RVCE Site-Wide Search Engine

A fast, full-text search engine built for RVCE's official website. It crawls HTML pages and PDFs using Scrapy, indexes content into Elasticsearch, and exposes a powerful search API using FastAPI.

---

## 🚀 Features

- 🔗 Crawls all internal links and PDFs from the RVCE website.
- 📄 Extracts and stores titles, content, and URLs.
- ⚡ Indexes 7000+ pages into Elasticsearch.
- 🧠 Fuzzy search with highlighting via FastAPI.
- 🌐 API-ready backend for integration into any frontend.
- 🌙 Dark-mode React frontend with keyboard-powered search (↵ Enter).

---

## 🗂️ Project Structure

```

rvce-search-engine/
├── backend/
│   └── elastic_client.py 
│   └── main.py               # FastAPI backend exposing /search endpoint
│   └── requirements.txt 
├── frontend/
├── crawler/
│   └── scrapy.cfg
│   └── crawler/         # Scrapy spider that crawls and dumps data
│       └── spiders
│           └── __init__.py
│           └── rvce_spider.py
│       ├── __init__.py
│       ├── items.py
│       ├── middlewares.py
│       ├── pipelines.py
│       ├── settings.py
├── data/
│   └── rvce_pages.json
│   └── rvce_pages_with_pdfs.json   # Output of crawler (HTML + PDFs)
├── indexer/
│   └── elastic_indexer.py    # Indexes data into Elasticsearch
├── pdf_parser/
│   └── extract_text.py
├── requirements.txt          # Python dependencies (backend + crawler)
└── README.md

````

---

## ⚙️ Requirements

- Python 3.9+
- Docker
- Elasticsearch 8.x or 9.x
- pip (Python package manager)

---

## 📦 Setup Instructions

### 1. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
````

### 2. Start Elasticsearch (via Docker)

```bash
docker run -d -p 9200:9200 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  elasticsearch:9.1.0
```

> ✅ You can also use `elasticsearch:8.12.0` if preferred (ensure Python client version matches).

### 3. Run the Scrapy Crawler

```bash
cd crawler
scrapy crawl rvce
```

This will crawl `rvce.edu.in` and extract structured page + PDF data into a JSON file.

### 4. Extract Text from PDFs

```bash
python pdf_parser/extract_text.py 
```

This extracts text from pdfs and merge into a clean format.

### 5. Index Data into Elasticsearch

```bash
python indexer/elastic_indexer.py
```

This loads the data file and populates the Elasticsearch index (`rvce`).


### 6. Run the FastAPI Backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

You can now access the search API at:

```
GET http://localhost:8000/search?q=your_query
```

### 7. Run the Frontend

```bash
npm install

npm run dev
```
You can now access the simple frontend with the Search feature.

---

## 🧪 Example API Query

```bash
curl "http://localhost:8000/search?query=admissions"
```

Returns:

```json
{
  "query": "admissions",
  "total": 10,
  "results": [
    {
      "title": "Online Fee Payment | R V College of Engineering",
      "url": "https://rvce.edu.in/Online-Fee-Payment",
      "score": 0.83,
      "snippet": "...Admissions open for..."
    }
  ]
}
```

---

## 🌐 Frontend

A dark-mode React + Vite-based frontend is available in the `frontend/` folder. It uses `fetch` to call the `/search` API.

---

## 📌 Notes

* The current project runs completely offline using crawled data.
* You can re-run the spider anytime to update the dataset.
* Fuzzy deduplication and scoring enhancements are included in the backend.

---

## 🙋‍♂️ Maintainer

Built by Ragav

---
