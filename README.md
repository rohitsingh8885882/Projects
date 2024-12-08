# Social Media Automation Bot

This project automates social media posts on Twitter and LinkedIn using AI-generated content based on trending news.

## Features

- Hourly automated posts to Twitter and LinkedIn
- GUI Dashboard for manual post management
- AI-generated content using OpenAI GPT-3.5
- Automatic hashtag generation
- Rate limiting and error handling
- Prometheus metrics for monitoring
- Docker and Heroku deployment support
- Logging system with rotation

## Local Setup

1. Create a `.env` file based on `.env.example`
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the automated bot:
   ```bash
   python social_media_bot.py
   ```
4. Run the GUI dashboard:
   ```bash
   streamlit run app.py
   ```

## Using the GUI Dashboard

1. Select topics from the sidebar
2. Click "Fetch Latest News" to get recent articles
3. Generate posts for specific articles
4. Review and edit generated content
5. Post directly to Twitter or LinkedIn with dedicated buttons
6. Monitor metrics in the sidebar

## Docker Deployment

1. Build and run using Docker Compose:
   ```bash
   docker-compose up -d
   ```

2. Monitor logs:
   ```bash
   docker-compose logs -f
   ```

## Heroku Deployment

1. Install Heroku CLI
2. Login to Heroku:
   ```bash
   heroku login
   ```

3. Create a new Heroku app:
   ```bash
   heroku create your-app-name
   ```

4. Set environment variables:
   ```bash
   heroku config:set OPENAI_API_KEY=your_key
   heroku config:set TWITTER_API_KEY=your_key
   # Set other environment variables...
   ```

5. Deploy to Heroku:
   ```bash
   git push heroku main
   ```

6. Scale the worker dyno:
   ```bash
   heroku ps:scale worker=1
   ```

## Monitoring

- Prometheus metrics available at `http://localhost:8000/metrics`
- GUI dashboard metrics visible in the sidebar
- Logs stored in `logs/bot.log` with rotation
- Monitor these metrics:
  - posts_generated_total
  - posts_failed_total
  - api_calls_total
  - api_latency_seconds

## Rate Limits

- Twitter: 50 tweets per 15-minute window
- LinkedIn: Unofficial API, use cautiously
- NewsAPI: 100 requests/day on free tier
- OpenAI: Varies by subscription

## Best Practices

- Monitor API usage and costs
- Review generated content regularly
- Keep backup logs
- Set up alerts for failed posts
- Regularly update dependencies