from fastapi import APIRouter
from app.services.robots import robots_checker

router = APIRouter()

@router.get("/tools/robots-check")
async def check_robots(url: str):
    """Check if a URL is crawlable."""
    can_crawl = await robots_checker.can_fetch(url)
    return {"url": url, "can_crawl": can_crawl}
