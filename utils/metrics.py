from prometheus_client import Counter, Gauge, start_http_server

# Metrics
posts_generated = Counter('posts_generated_total', 'Total number of posts generated')
posts_failed = Counter('posts_failed_total', 'Total number of failed posts')
api_calls = Counter('api_calls_total', 'Total number of API calls', ['api_name'])
api_latency = Gauge('api_latency_seconds', 'API call latency', ['api_name'])

def init_metrics(port=8000):
    start_http_server(port)