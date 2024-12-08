import time
from functools import wraps

class RateLimiter:
    def __init__(self, calls_per_hour):
        self.calls_per_hour = calls_per_hour
        self.calls = []
    
    def can_make_request(self):
        current_time = time.time()
        hour_ago = current_time - 3600
        
        # Remove calls older than 1 hour
        self.calls = [call for call in self.calls if call > hour_ago]
        
        return len(self.calls) < self.calls_per_hour
    
    def add_request(self):
        self.calls.append(time.time())

def rate_limit(calls_per_hour):
    limiter = RateLimiter(calls_per_hour)
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            while not limiter.can_make_request():
                time.sleep(60)  # Wait for 1 minute
            limiter.add_request()
            return func(*args, **kwargs)
        return wrapper
    return decorator