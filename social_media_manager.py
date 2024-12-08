import tweepy
from linkedin_api import Linkedin
from config import (
    TWITTER_API_KEY, TWITTER_API_SECRET,
    TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET,
    LINKEDIN_EMAIL, LINKEDIN_PASSWORD
)

class SocialMediaManager:
    def __init__(self):
        # Initialize Twitter
        auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
        self.twitter_api = tweepy.API(auth)
        
        # Initialize LinkedIn
        self.linkedin_api = Linkedin(LINKEDIN_EMAIL, LINKEDIN_PASSWORD)

    def post_to_twitter(self, content, hashtags):
        try:
            full_post = f"{content}\n\n{hashtags}"
            self.twitter_api.update_status(full_post)
            print("Successfully posted to Twitter!")
        except Exception as e:
            print(f"Error posting to Twitter: {str(e)}")

    def post_to_linkedin(self, content, hashtags):
        try:
            full_post = f"{content}\n\n{hashtags}"
            self.linkedin_api.post(text=full_post)
            print("Successfully posted to LinkedIn!")
        except Exception as e:
            print(f"Error posting to LinkedIn: {str(e)}")