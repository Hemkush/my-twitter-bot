# scraper/rss_fetcher.py
import feedparser

def fetch_rss_feed(url, limit=10):
    feed = feedparser.parse(url)
    return [
        {"title": entry.title, "url": entry.link}
        for entry in feed.entries[:limit]
    ]

def fetch_techcrunch_ai():
    return fetch_rss_feed(
        "https://techcrunch.com/category/artificial-intelligence/feed/"
    )


