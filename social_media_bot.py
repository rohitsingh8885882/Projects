import schedule
import time
from news_fetcher import NewsFetcher
from content_generator import ContentGenerator
from social_media_manager import SocialMediaManager
from utils.logger import setup_logger
from utils.metrics import init_metrics, posts_generated, posts_failed
import os

logger = setup_logger()

def post_update():
    try:
        logger.info("Starting post update cycle")
        news_fetcher = NewsFetcher()
        content_generator = ContentGenerator()
        social_media = SocialMediaManager()

        articles = news_fetcher.get_trending_news()
        
        for article in articles:
            try:
                post_content = content_generator.generate_post(article)
                if not post_content:
                    continue
                    
                hashtags = content_generator.generate_hashtags(post_content, article)
                
                social_media.post_to_twitter(post_content, hashtags)
                social_media.post_to_linkedin(post_content, hashtags)
                
                posts_generated.inc()
                logger.info(f"Successfully posted content about: {article['title']}")
                
                # Wait between posts to avoid rate limits
                time.sleep(300)  # 5 minutes
                
            except Exception as e:
                posts_failed.inc()
                logger.error(f"Error processing article {article['title']}: {str(e)}")
                continue
                
    except Exception as e:
        logger.error(f"Error in post update cycle: {str(e)}")

def main():
    logger.info("Starting Social Media Bot...")
    
    # Initialize metrics server
    init_metrics(port=int(os.getenv('METRICS_PORT', '8000')))
    
    # Schedule posts to run every hour
    schedule.every().hour.do(post_update)
    
    # Run first post immediately
    post_update()
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()