import openai
from config import OPENAI_API_KEY

class ContentGenerator:
    def __init__(self):
        openai.api_key = OPENAI_API_KEY

    def generate_post(self, article):
        try:
            # Create a prompt for OpenAI
            prompt = f"""
            Article Title: {article['title']}
            Article Description: {article['description']}
            
            Create a professional and engaging social media post about this news article.
            Include a brief analysis and your thoughts.
            Keep it under 280 characters for Twitter compatibility.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional social media manager and tech analyst."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating content: {str(e)}")
            return None

    def generate_hashtags(self, post_content, article):
        try:
            prompt = f"""
            Post: {post_content}
            Article Title: {article['title']}
            
            Generate 3-5 relevant and trending hashtags for this post.
            Return only the hashtags separated by spaces.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Generate relevant hashtags for social media posts."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating hashtags: {str(e)}")
            return ""