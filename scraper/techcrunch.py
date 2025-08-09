# import requests
# from bs4 import BeautifulSoup

# def fetch_techcrunch_ai():
#     url = "https://techcrunch.com/tag/artificial-intelligence/feed/"
#     headers = {'User-Agent': 'Mozilla/5.0'}
#     resp = requests.get(url)
#     soup = BeautifulSoup(resp.text, 'html.parser')
#     articles = []
#     for article in soup.find_all("a", class_="post-block__title__link", href=True)[0:1]:
#         title = article.get_text(strip=True)
#         link = article['href']
#         if title and link:
#             articles.append({"title": title, "url": link})
#     for article in articles:
#         print(f"Title: {article['title']}")
#         print(f"URL: {article['url']}")
#         print("------------------------")
#     return articles

import requests
from bs4 import BeautifulSoup

def fetch_techcrunch_ai():
    url = "https://www.bloomberg.com/technology"
    headers = {"Accept": "text/html"}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    titles = soup.find_all("h3" , class_="SectionFrontHeaderBrand_title__RyJct")
    print("Found articles on TechCrunch AI.", titles)
    # articles = []
    # for article in titles[0:10]:
    #     title = article.get_text(strip=True)
    #     articles.append(title)
    #     print(f"Title: {title}")
        
    # return articles

if __name__ == "__main__":
    """
    Initialize the fetcher module.
    """
    print("TechCrunch AI fetcher initialized.")
    fetch_techcrunch_ai()