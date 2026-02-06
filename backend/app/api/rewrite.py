from fastapi import APIRouter
from app.services.ai_optimizer import ai_optimizer

router = APIRouter()

@router.post("/rewrite")
async def rewrite_meta(page_data: dict, keyword: str):
    """Optimize meta tags and titles using AI."""
    return await ai_optimizer.optimize_content(page_data, keyword)
