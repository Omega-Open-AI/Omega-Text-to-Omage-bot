"""
Metrics configuration for Modal deployment.
"""

from prometheus_client import Counter, Histogram, Summary

# Request metrics
TOTAL_REQUESTS = Counter(
    'omega_bot_requests_total',
    'Total number of requests processed'
)

FAILED_REQUESTS = Counter(
    'omega_bot_requests_failed_total',
    'Total number of failed requests'
)

# Image generation metrics
GENERATION_TIME = Histogram(
    'omega_bot_image_generation_seconds',
    'Time spent generating images',
    buckets=[1, 2, 5, 10, 20, 30, 60]
)

GENERATION_FAILURES = Counter(
    'omega_bot_generation_failures_total',
    'Total number of image generation failures'
)

# Memory metrics
MEMORY_USAGE = Summary(
    'omega_bot_memory_usage_bytes',
    'Memory usage in bytes'
)

# Rate limiting metrics
RATE_LIMITS_HIT = Counter(
    'omega_bot_rate_limits_total',
    'Total number of rate limit hits'
)
