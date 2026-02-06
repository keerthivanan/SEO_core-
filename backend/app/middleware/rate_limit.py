"""
Enterprise-grade rate limiting for RankForge AI
Prevents API abuse and ensures fair usage
"""

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, Response
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> Response:
    """
    Custom handler for rate limit exceeded errors
    Enterprise-grade error response
    """
    logger.warning(
        f"RATE_LIMIT_EXCEEDED: IP {get_remote_address(request)} exceeded rate limit",
        extra={
            "ip": get_remote_address(request),
            "path": request.url.path,
            "method": request.method
        }
    )
    
    return JSONResponse(
        status_code=429,
        content={
            "error": "Rate limit exceeded",
            "message": "Too many requests. Please slow down and try again in a few moments.",
            "retry_after": "60 seconds",
            "upgrade": "Consider upgrading to Pro for higher limits"
        },
        headers={"Retry-After": "60"}
    )

# Rate limit configurations for different tiers
class RateLimits:
    """Enterprise SaaS rate limits"""
    FREE_TIER = "10/minute"  # Free users
    PRO_TIER = "100/minute"  # Pro users
    ENTERPRISE_TIER = "1000/minute"  # Enterprise users
    API_DEFAULT = "100/minute"  # Default for API endpoints
