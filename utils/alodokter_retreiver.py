import json
import requests
import urllib.parse

from bs4 import BeautifulSoup
from trafilatura import fetch_url, bare_extraction


class AlodokterRetreiver:
    @staticmethod
    def get_article(url):
        
        if 'komunitas' in url:
            html = requests.get(url).text
            soup = BeautifulSoup(html, "html.parser")
            article = soup.find("doctor-topic").get("doctor-topic-content")
            return article
        
        else:
            html = fetch_url(url)
            article = (
                bare_extraction(html)["text"]
                if (
                    bare_extraction(html)["text"] is not None
                    and bare_extraction(html)["text"] != ""
                )
                else bare_extraction(html)["raw_text"]
            )
            return article

    @staticmethod
    def search_articles(query):
        query = urllib.parse.quote(query)
        url = f"https://www.alodokter.com/search?s={query}"
        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("card-post-index")
        article_data = []

        for article in articles:

            data = {
                'title': article.get("title"),
                'url': f"https://www.alodokter.com{article.get('url-path')}",
            }

            article_data.append(data)

        return article_data