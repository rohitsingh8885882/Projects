import streamlit as st
from news_fetcher import NewsFetcher
from content_generator import ContentGenerator
from social_media_manager import SocialMediaManager
from utils.logger import setup_logger
from utils.metrics import posts_generated, posts_failed

logger = setup_logger()

def main():
    st.set_page_config(page_title="Social Media Automation Dashboard", layout="wide")
    st.title("Social Media Automation Dashboard")

    # Initialize components
    news_fetcher = NewsFetcher()
    content_generator = ContentGenerator()
    social_media = SocialMediaManager()

    # Topic Selection
    st.sidebar.header("Settings")
    selected_topics = st.sidebar.multiselect(
        "Select Topics",
        ["AI", "Technology", "Programming", "Data Science", "Web Development", 
         "Cybersecurity", "Cloud Computing", "Blockchain", "IoT", "Machine Learning"],
        default=["AI", "Technology", "Programming"]
    )

    # Main content area
    col1, col2 = st.columns(2)

    with col1:
        st.header("News Articles")
        if st.button("Fetch Latest News"):
            with st.spinner("Fetching news..."):
                articles = news_fetcher.get_trending_news()
                if articles:
                    for idx, article in enumerate(articles):
                        with st.expander(f"📰 {article['title']}", expanded=True):
                            st.write(article['description'])
                            if st.button(f"Generate Post {idx + 1}"):
                                with st.spinner("Generating content..."):
                                    post_content = content_generator.generate_post(article)
                                    hashtags = content_generator.generate_hashtags(post_content, article)
                                    if post_content:
                                        st.session_state[f'post_{idx}'] = {
                                            'content': post_content,
                                            'hashtags': hashtags
                                        }
                                        st.success("Content generated!")

    with col2:
        st.header("Generated Posts")
        for idx in range(len(getattr(st.session_state, 'articles', []))):
            if f'post_{idx}' in st.session_state:
                post = st.session_state[f'post_{idx}']
                with st.expander(f"Post {idx + 1}", expanded=True):
                    st.text_area("Content", post['content'], height=100, key=f'content_{idx}')
                    st.text_area("Hashtags", post['hashtags'], height=50, key=f'hashtags_{idx}')
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"Post to Twitter {idx + 1}"):
                            try:
                                social_media.post_to_twitter(post['content'], post['hashtags'])
                                posts_generated.inc()
                                st.success("Posted to Twitter!")
                            except Exception as e:
                                posts_failed.inc()
                                st.error(f"Error posting to Twitter: {str(e)}")
                    
                    with col2:
                        if st.button(f"Post to LinkedIn {idx + 1}"):
                            try:
                                social_media.post_to_linkedin(post['content'], post['hashtags'])
                                posts_generated.inc()
                                st.success("Posted to LinkedIn!")
                            except Exception as e:
                                posts_failed.inc()
                                st.error(f"Error posting to LinkedIn: {str(e)}")

    # Metrics Display
    st.sidebar.header("Metrics")
    st.sidebar.metric("Posts Generated", int(posts_generated._value.get()))
    st.sidebar.metric("Posts Failed", int(posts_failed._value.get()))

if __name__ == "__main__":
    main()