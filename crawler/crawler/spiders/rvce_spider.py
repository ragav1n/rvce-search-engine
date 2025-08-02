import scrapy
from urllib.parse import urljoin
from bs4 import BeautifulSoup

class RVCESpider(scrapy.Spider):
    name = "rvce"
    allowed_domains = ["rvce.edu.in"]
    start_urls = ["https://rvce.edu.in"]

    def parse(self, response):
        content_type = response.headers.get("Content-Type", b"").decode("utf-8", errors="ignore")

        # ✅ Handle PDFs separately (just yield the link as a record)
        if response.url.lower().endswith(".pdf"):
            yield {
                "url": response.url,
                "title": response.url.split("/")[-1],
                "content": ""  # to be filled by PDF parser later
            }
            return

        # ✅ Only parse HTML
        if "text/html" not in content_type:
            return

        soup = BeautifulSoup(response.text, "lxml")
        title = soup.title.string.strip() if soup.title else ""
        text = ' '.join(soup.stripped_strings)

        yield {
            "url": response.url,
            "title": title,
            "content": text
        }

        # ✅ Follow all internal links (HTML + PDFs)
        for href in response.css('a::attr(href)').getall():
            if href.startswith(("mailto:", "javascript:", "tel:")):
                continue

            url = urljoin(response.url, href)
            if url.startswith("http") and "rvce.edu.in" in url:
                yield response.follow(url, callback=self.parse)
