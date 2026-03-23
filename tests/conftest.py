import pytest


@pytest.fixture(autouse=True)
def clear_throttle_cache():
    """Clear DRF throttle cache before each test."""
    from django.core.cache import cache

    cache.clear()
    yield
    cache.clear()
