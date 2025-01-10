import wikipediaapi
import requests

class WikipediaAPI:
    def __init__(self, language='fr', user_agent='SearchEngineProject/1.0 (yasminemaddouri25@gmail.com)'):
        self.language = language
        self.user_agent = user_agent
        
        # Initialiser l'API avec l'agent utilisateur
        self.wiki = wikipediaapi.Wikipedia(
            language=self.language,
            user_agent=self.user_agent,
            
        )

    def get_articles(self, keyword, max_articles=100):
        results = []
        page = self.wiki.page(keyword)

        if page.exists():
            sections = page.text.split('\n\n')[:max_articles]  # Diviser en sections
            for idx, section in enumerate(sections):
                results.append({
                    'id': f'wikipedia_{idx}',
                    'title': page.title,
                    'text': section,
                    'author': None,
                    'date': None,
                    'url': page.fullurl,
                    'source': 'wikipedia'
                })
        return results


class NewsAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2/everything"

    def get_articles(self, keyword, max_articles=100, language='fr'):
        params = {
            'q': keyword,
            'apiKey': self.api_key,
            'pageSize': max_articles,
            'language': language
        }
        response = requests.get(self.base_url, params=params)
        articles = []

        if response.status_code == 200:
            data = response.json()
            for idx, article in enumerate(data['articles']):
                articles.append({
                    'id': f'news_{idx}',
                    'title': article['title'],
                    'text': article['description'] or article['content'],
                    'author': article['author'],
                    'date': article['publishedAt'],
                    'url': article['url'],
                    'source': 'newsapi'
                })
        return articles

