from newsapi import NewsApiClient
from config import NEWS_API_KEY, TOPICS
from datetime import datetime, timedelta

class NewsFetcher:
    def __init__(self):
        self.newsapi = NewsApiClient(api_key=NEWS_API_KEY)

    def get_trending_news(self):
        try:
            # Get news from the last 24 hours
            yesterday = datetime.now() - timedelta(days=1)
            
            articles = []
            for topic in TOPICS:
                response = self.newsapi.get_everything(
                    q=topic,
                    language='en',
                    from_param=yesterday.strftime('%Y-%m-%d'),
                    sort_by='relevancy'
                )
                
                if response['articles']:
                    # Get the most relevant article for each topic
                    articles.append(response['articles'][0])
            
            return articles
        except Exception as e:
            print(f"Error fetching news: {str(e)}")
            return []