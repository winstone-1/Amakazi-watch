from django.utils.cache import patch_response_headers
from django.utils.decorators import decorator_from_middleware
import hashlib
import json


def add_cache_headers(response, max_age=300):
    """Add ETag and Cache-Control headers for offline support."""
    if hasattr(response, "data"):
        content = json.dumps(response.data, default=str).encode()
        etag = hashlib.md5(content).hexdigest()
        response["ETag"] = f'"{etag}"'
        response["Cache-Control"] = f"public, max-age={max_age}"
        response["Vary"] = "Accept, Authorization"
    return response
